import copy
import json
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageToolCall

from .types import Response, Agent, AgentFunction, FunctionResult
from .util import debug_print, function_to_json

# 用来存储上下文变量的key名字
__CTX_VARS_NAME__ = "context_variables"


class Swarm:
    def __init__(self, client=None):
        if not client:
            client = OpenAI()
        self.client = client

    def get_chat_completion(
            self,
            agent: Agent,
            history: List,
            context_variables: dict,
            model_override: str,
            stream: bool,
            debug: bool
    ) -> ChatCompletion:
        """
        执行LLM的chat completion
        :param agent: 执行的 agent
        :param history: 执行的历史会话，用来添加到 chat 的 messages 中
        :param context_variables: 上下文变量
        :param model_override: 用来覆盖运行的 model 。为 None 的时候，会使用 agent 中的 model
        :param stream: 是否是 stream
        :param debug: 是否是 debug
        :return:
        """
        instructions = (
            agent.instructions(context_variables)
            if callable(agent.instructions)
            else agent.instructions
        )
        messages = [{"role": "system", "content": instructions}] + history
        debug_print(debug, "Getting chat completion for:", str(messages))

        # 要排除不转成json的变量名
        exclude_function_param_names = [__CTX_VARS_NAME__]
        tools = [function_to_json(f, exclude_function_param_names) for f in agent.functions]
        tool_choice = function_to_json(agent.function_chosen, exclude_function_param_names)

        create_params = {
            "model": model_override or agent.model,
            "messages": messages,
            "tools": tools or None,
            "tool_choice": tool_choice or None,
            "stream": stream
        }

        return self.client.chat.completions.create(**create_params)

    def handle_function_result(
            self,
            result,
            debug
    ) -> FunctionResult:
        match result:
            case FunctionResult() as result:
                return result
            case Agent() as agent:
                return FunctionResult(
                    value=json.dumps({"assistant": agent.name}),
                    agent=agent
                )
            case _:
                try:
                    return FunctionResult(value=str(result))
                except Exception as e:
                    error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
                    debug_print(debug, error_message)
                    raise TypeError(error_message)
    def handle_tool_calls(
            self,
            tool_calls: List[ChatCompletionMessageToolCall],
            functions: List[AgentFunction],
            context_variables: dict,
            debug: bool
    ) -> Response:
        """
        处理 LLM 返回的结果
        :param tool_calls: LLM 返回的结果
        :param functions: 所有可选的 function
        :param context_variables: 上下文参数
        :param debug: 是否是 debug
        :return:
        """
        function_map = {f.__name__: f for f in functions}
        partial_response = Response(
            messages=[], agent=None, context_variables={}
        )

        for tool_call in tool_calls:
            # LLM 返回的，需要执行的 function 的名字
            name = tool_call.function.name
            # 如果 LLM 返回的 name 在可选的函数列表中不存在，那么就跳过
            if name not in function_map:
                debug_print(debug, f"Tool {name} not found in function map")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "tool_name": name,
                        "content": f"Error: Tool {name} not found"
                    }
                )
                continue
            # LLM 返回的用来执行函数的参数
            args = json.loads(tool_call.function.arguments)
            debug_print(debug, f"Processing tool call: {name} with arguments {args}")
            func: AgentFunction = function_map[name]
            # 将 上下文变量 也添加到函数的参数中
            if __CTX_VARS_NAME__ in func.__code__.co_varnames:
                args[__CTX_VARS_NAME__] = context_variables
            # 执行函数
            raw_func_result = func(**args)
            # 处理函数执行的结果，函数执行的结果，可能是字符串，也有可能是另一个Agent
            result: FunctionResult = self.handle_function_result(raw_func_result, debug)
            partial_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "tool_name": name,
                    "content": result.value
                }
            )
            partial_response.context_variables.update(result.context_variables)
            if result.agent:
                partial_response.agent = result.agent

        return partial_response

    def run(
            self,
            agent: Agent,
            messages: List,
            context_variables: dict = {},
            model_override: str = None,
            stream: bool = False,
            debug: bool = False,
            max_turns: int = float("inf"),
            execute_tools: bool = True,
    ) -> Response:
        active_agent = agent
        context_variables = copy.deepcopy(context_variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        while len(history) - init_len < max_turns and active_agent:
            # 传入历史记录、上下文变量等参数，来启动agent
            completion = self.get_chat_completion(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                model_override=model_override,
                stream=stream,
                debug=debug
            )
            message = completion.choices[0].message
            debug_print(debug, "Received completion:", str(message))
            message.sender = active_agent.name
            history.append(
                json.loads(message.model_dump_json())
            )

            if not execute_tools or not message.tool_calls:
                debug_print(debug, "Ending turn.")
                break

            # 处理函数调用，更新上下文变量，转换agent
            partial_response = self.handle_tool_calls(
                message.tool_calls, active_agent.functions, context_variables, debug
            )
            history.extend(partial_response.messages)
            context_variables.update(partial_response.context_variables)

            # 如果 执行结果返回中的 agent 不存在，那么就跳出循环
            # 否则，就就替换成新的agent
            if not partial_response.agent:
                break
            active_agent = partial_response.agent

        return Response(
            messages=history,
            agent=active_agent,
            context_variables=context_variables
        )

