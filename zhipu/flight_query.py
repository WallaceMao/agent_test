import json
import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ.get("DEFAULT_MODEL")

client = ZhipuAI()
print(f"===》 模型信息： {MODEL} {os.environ.get('ZHIPUAI_API_KEY')} \n")

def get_flight_number(date:str , departure:str , destination:str):
    print(f"====> get_flight_number: {date}: {departure}->{destination}\n")
    flight_number = {
        "北京":{
            "上海" : "1234",
            "广州" : "8321",
        },
        "上海":{
            "北京" : "1233",
            "广州" : "8123",
        }
    }
    return { "flight_number":flight_number[departure][destination] }
def get_ticket_price(date:str , flight_number:str):
    return {
        "1233": {"ticket_price": "71233"},
        "1234": {"ticket_price": "71234"},
        "8321": {"ticket_price": "78321"},
        "8123": {"ticket_price": "78123"},
        }.get(flight_number, None)

def parse_function_call(model_response,messages):
    # 处理函数调用结果，根据模型返回参数，调用对应的函数。
    # 调用函数返回结果后构造tool message，再次调用模型，将函数结果输入模型
    # 模型会将函数调用结果以自然语言格式返回给用户。
    if model_response.choices[0].message.tool_calls:
        tool_call = model_response.choices[0].message.tool_calls[0]
        args = tool_call.function.arguments
        function_result = {}
        if tool_call.function.name == "get_flight_number":
            function_result = get_flight_number(**json.loads(args))
        if tool_call.function.name == "get_ticket_price":
            function_result = get_ticket_price(**json.loads(args))
        messages.append({
            "role": "tool",
            "content": f"{json.dumps(function_result)}",
            "tool_call_id":tool_call.id
        })
        response = client.chat.completions.create(
            model=MODEL,  # 填写需要调用的模型名称
            messages=messages,
            tools=tools,
        )
        messages.append(response.choices[0].message.model_dump())

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_number",
            "description": "根据始发地、目的地和日期，查询对应日期的航班号",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure": {
                        "description": "出发地",
                        "type": "string"
                    },
                    "destination": {
                        "description": "目的地",
                        "type": "string"
                    },
                    "date": {
                        "description": "日期",
                        "type": "string",
                    }
                },
                "required": [ "departure", "destination", "date" ]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "查询某航班在某日的票价",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "description": "航班号",
                        "type": "string"
                    },
                    "date": {
                        "description": "日期",
                        "type": "string",
                    }
                },
                "required": [ "flight_number", "date"]
            },
        }
    },
]

messages = []
 
messages.append({"role": "system", "content": "不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息"})
messages.append({"role": "user", "content": "帮我查询今天，上海去北京的飞机"})
response = client.chat.completions.create(
    model=MODEL,  # 填写需要调用的模型名称
    messages=messages,
    tools=tools,
)
# print(response.choices[0].message)
print(f"====> 航班信息返回： {response}\n")
messages.append(response.choices[0].message.model_dump())
 
parse_function_call(response,messages)

print(f"====> 航班信息: {messages}\n")

# 查询票价
messages.append({"role": "user", "content": "这趟航班的价格是多少？"})
response = client.chat.completions.create(
    model=MODEL,  # 填写需要调用的模型名称
    messages=messages,
    tools=tools,
)
print(f"====> 价格信息返回: {response}\n")
messages.append(response.choices[0].message.model_dump())
 
parse_function_call(response,messages)
print(f"====> 价格信息: {messages}\n")