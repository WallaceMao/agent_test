import os

from utils.setup import setup_langchain
from utils.logger import setup_logger
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

setup_langchain()
logger = setup_logger()

load_dotenv()

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = ChatOpenAI(model=DEFAULT_MODEL)

chat_history = []

system_message = SystemMessage(content="你是一个好用的AI助手。")
chat_history.append(system_message)

while True:
    query = input("你：")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    print(f"AI： {response}")

print("======= 消息历史 ========")
print(chat_history)

