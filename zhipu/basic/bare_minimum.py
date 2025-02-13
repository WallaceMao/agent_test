from ..myswarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()

agent = Agent(
    name="我的智能体",
    instructions="你是一个非常有用的agent。"
)

messages = [{"role": "user", "content": "你好！"}]
response = client.run(agent=agent, messages=messages, debug=True)

print(response)
