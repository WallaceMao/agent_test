from ..myswarm import Swarm, Agent
from dotenv import load_dotenv

load_dotenv()

client = Swarm()


def instructions(context_variables):
    name = context_variables.get("name", "User")
    context_variables["from_instructions"] = "INSTRUCTIONS"
    return f"You are a helpful agent. Greet the user by name ({name})."


def print_account_details(context_variables: dict):
    user_id = context_variables.get("user_id", None)
    name = context_variables.get("name", None)
    context_variables["from_print_account_detail"] = "PRINT_ACCOUNT_DETAIL"
    print(f"Account Details: {name} {user_id}")
    return "Success"


agent = Agent(
    name="Agent",
    instructions=instructions,
    functions=[print_account_details],
)

context_variables = {"name": "James", "user_id": 123}

response = client.run(
    messages=[{"role": "user", "content": "Hi!"}],
    agent=agent,
    context_variables=context_variables,
    debug=True,
)
print(response.messages[-1]["content"])
print(response.context_variables)

response = client.run(
    messages=[{"role": "user", "content": "Print my account details!"}],
    agent=agent,
    context_variables=context_variables,
    debug=True,
)
print(response.messages[-1]["content"])
print(response.context_variables)
