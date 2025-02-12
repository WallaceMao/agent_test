import os
from swarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()

agent = Agent(
    name="Agent",
    model=os.environ.get("SWARM_DEFAULT_MODEL"),
    instructions="You are a helpful agent."
)

messages = [{"role": "user", "content": "Hi!"}]
stream = client.run(agent=agent, messages=messages, stream=True)

full_answer = ""
for chunk in stream:
    if "response" in chunk:
        full_answer = chunk.get('response', 'no data')

print(full_answer)
