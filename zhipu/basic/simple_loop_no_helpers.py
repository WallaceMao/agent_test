from ..myswarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()

my_agent = Agent(
    name="Agent",
    instructions="You are a helpful agent."
)


def pretty_print_messages(messages):
    for message in messages:
        if message["content"] is None:
            continue
        print(f"{message.get('sender', 'You')}: {message['content']}")


messages = []
agent = my_agent
while True:
    user_input = input("> ")
    messages.append({"role": "user", "content": user_input})

    resp = client.run(agent=agent, messages=messages, debug=True)
    messages = resp.messages
    agent = resp.agent
    pretty_print_messages(messages)
