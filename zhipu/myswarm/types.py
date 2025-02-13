from typing import Union, Callable, List, Optional

from pydantic import BaseModel


# 注意，这里的 Callable 的返回值中 Agent 是在之后才会定义的，
# 所以这里需要使用 pydantic 的 forward annotation 特性，使用字符串来表示 Agent，防止解释器报错
AgentFunction = Callable[[], Union[str, 'Agent', dict]]


class Agent(BaseModel):
    name: str = "智能体"
    model: str = "glm-4"
    instructions: Union[str, Callable[[], str]] = "你是一个有用的智能体",
    functions: List[AgentFunction] = []
    function_chosen: AgentFunction = None


class Response(BaseModel):
    messages: List = []
    agent: Optional[Agent] = None
    context_variables: dict = {}


class FunctionResult(BaseModel):
    """
    agent 函数的执行的结果，结果可能是字符串，也可能是另一个Agent
    """
    value: str = ""
    agent: Agent = None
    context_variables: dict = {}
