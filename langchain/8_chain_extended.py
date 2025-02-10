import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

model = ChatOpenAI(model=os.environ.get("DEFAULT_MODEL"))

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes."),
])

# 转换为大写
uppercase_output = RunnableLambda(lambda x: x.upper())
# 统计单词数量
count_words = RunnableLambda(lambda x: f"Word count: {len(x.split())}\n{x}")

chain = prompt_template | model | StrOutputParser() | uppercase_output | count_words

result = chain.invoke({"topic": "lawyers", "joke_count": 3})

print(result)
