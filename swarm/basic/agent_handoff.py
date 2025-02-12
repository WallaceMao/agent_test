import os
from swarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()

english_agent = Agent(
    name="English Agent",
    model=os.environ.get("SWARM_DEFAULT_MODEL"),
    instructions="You only speak English. 你只会说英语。"
)

chinese_agent = Agent(
    name="Chinese Agent",
    model=os.environ.get("SWARM_DEFAULT_MODEL"),
    instructions="You only speak Chinese. 你只会说汉语。"
)


def transfer_to_chinese_agent():
    """Transfer Chinese-speaking users immediately"""
    return chinese_agent


english_agent.functions.append(transfer_to_chinese_agent)


messages = [{"role": "user", "content": "你好，你是谁？"}]
stream = client.run(agent=english_agent, messages=messages, stream=True, debug=True)

# 返回结果
full_answer = ""
for chunk in stream:
    if "response" in chunk:
        full_answer = chunk.get('response', 'no data')

print(full_answer)
