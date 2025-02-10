from utils.setup import setup_langchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

setup_langchain()
load_dotenv()

model = ChatOpenAI(model="deepseek-chat")

result = model.invoke("81除以9是多少？")

print(f"Full result {result}")
print(f"Content result {result.content}")
