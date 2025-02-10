import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableSequence

load_dotenv()

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = ChatOpenAI(model=DEFAULT_MODEL)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个会讲{topic}笑话的喜剧演员"),
    ("human", "给我讲{count}个笑话")
])

format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
invoke_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
parse_output = RunnableLambda(lambda x: x.content)

chain = RunnableSequence(first=format_prompt, middle=[invoke_model], last=parse_output)

resp = chain.invoke({"topic": "医生", "count": 2})

print(resp)
