import os
from swarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()


def instructions(variables: dict):
    name = variables.get("name", "NO_NAME")
    print(f"====> name in instructions: {name}")
    return f"你是一个好用的助手，欢迎用户： {name}"


def print_account_details(variables: dict):
    user_id = variables.get("user_id", None)
    name = variables.get("name", None)
    print(f"====> account detail: {name}, {user_id}")
    return "success"


agent = Agent(
    name="Agent",
    model=os.environ.get("DEFAULT_MODEL"),
    instructions=instructions,
    functions=[print_account_details]
)


context_variables = {"name": "Wallace", "user_id": 98989}
response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "你好！"}],
    context_variables=context_variables,
    stream=False,
    debug=True)

print(f"---> 你好： {response.messages[-1]['content']}")

# response = client.run(
#     agent=agent,
#     messages=[{"role": "user", "content": "print my account detail!"}],
#     context_variables=context_variables,
#     stream=False,
#     debug=True)
#
# print(f"---> 打印账户信息： {response.messages[-1]['content']}")
