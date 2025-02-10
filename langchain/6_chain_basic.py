import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = ChatOpenAI(model=DEFAULT_MODEL)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个会讲{topic}笑话的喜剧演员"),
    ("human", "给我讲{count}个笑话")
])

chain = prompt_template | model | StrOutputParser()

result = chain.invoke({"topic": "医生", "count": 3})

print(result)

