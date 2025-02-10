import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch
from langchain.schema.runnable import RunnableLambda

load_dotenv()

model = ChatOpenAI(model=os.environ.get("DEFAULT_MODEL"))

classification_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个聪明的客服人员"),
    ("human", "这个一个用户反馈，请根据反馈的情绪，将反馈分类成 积极 消极 中立 其他 四种： {feedback}")
])

positive_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个擅长鼓励的客服人员"),
    ("human", "根据这个积极的反馈，生成一条带有感谢、鼓励等情绪的回复: {feedback}")
])

negative_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个擅长安抚客户的客服人员"),
    ("human", "根据这个消极的反馈，生成一条安抚用户情绪的回复: {feedback}")
])

neutral_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个聪明的客服人员"),
    ("human", "根据这个中立的反馈，生成一条回复: {feedback}")
])

default_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个聪明的客服人员"),
    ("human", "根据这个反馈，生成一条回复: {feedback}")
])

branches = RunnableBranch(
    (
        lambda x: "积极" in x,
        positive_feedback_template | model | StrOutputParser()
    ),
    (
        lambda x: "消极" in x,
        negative_feedback_template | model | StrOutputParser()
    ),
    (
        lambda x: "中立" in x,
        neutral_feedback_template | model | StrOutputParser()
    ),
    default_feedback_template | model | StrOutputParser()
)


def print_and_return(x):
    print(f"====> content: {x}")
    return x


classification_chain = classification_template | model | StrOutputParser()

chain = classification_chain | RunnableLambda(lambda x: print_and_return(x)) | branches

review = "你们产品问题很大，不好用，我要求退款"
result = chain.invoke({"feedback": review})

print(result)