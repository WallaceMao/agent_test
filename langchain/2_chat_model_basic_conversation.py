import os
from utils.setup import setup_langchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from utils.logger import setup_logger

setup_langchain()
logger = setup_logger()
load_dotenv()

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = ChatOpenAI(model=DEFAULT_MODEL)

messages = [
    SystemMessage(content="计算下面的这个数学问题"),
    HumanMessage(content="49除以7等于多少？")
]

result = model.invoke(messages)

logger.info(f"AI的回答: {result.content}")

