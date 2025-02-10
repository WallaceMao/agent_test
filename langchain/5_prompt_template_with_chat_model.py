import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = ChatOpenAI(model=DEFAULT_MODEL)

print("======== Prompt from template ========")
template = "给我将一个有关{topic}的笑话"
prompt_template = ChatPromptTemplate.from_template(template)
prompt = prompt_template.invoke({"topic": "猫"})
result = model.invoke(prompt)
print(result.content)

template_multiple = """
你是一个有用的助手。
人类： 给我将一个{adjective}的关于{animal}故事
助手："""

prompt_multiple = ChatPromptTemplate.from_template(template_multiple)
prompt = prompt_multiple.invoke({"adjective": "恐怖", "animal": "狗"})
print("======== Prompt from multiple template ========")
print(prompt)
result = model.invoke(prompt)
print(result.content)

messages = [
    ("system", "你是一个会将关于{topic}的故事的喜剧演员"),
    ("human", "给我将{joke_count}个笑话")
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic": "律师", "joke_count": 2})
print("======== Prompt from Human and System message ========")
print(prompt)
result = model.invoke(prompt)
print(result.content)
