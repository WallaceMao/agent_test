from ..myswarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()

english_agent = Agent(
    name="英文问题回答智能体",
    instructions="我只会回答英语问题",
)

chinese_agent = Agent(
    name="中文问题回答智能体",
    instructions="我只会回答中文问题",
)


def transfer_to_english_agent():
    """移交给可以讲英语的智能体"""
    return english_agent


chinese_agent.functions.append(transfer_to_english_agent)

messages = [{"role": "user", "content": "Hello! What is your name?"}]
response = client.run(agent=chinese_agent, messages=messages, debug=True)

print(response.messages)
print(f"===> 返回结果： {response.messages[-1]['content']}")
