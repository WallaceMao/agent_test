import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser

load_dotenv()
model = ChatOpenAI(model=os.environ.get("DEFAULT_MODEL"))

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个产品评估专家"),
    ("human", "列出这个产品的主要特点：{product_name}")
])


# 分析优点
def analyze_pros(features):
    pros_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个产品评估专家"),
        ("human", "给定以下特点： {features}，列举出其中的优点")
    ])
    # return pros_template.format_prompt(features=features)
    print(f"---> analyze_pros before format: \n{pros_template}")
    analyze_pros_result = pros_template.format_prompt(features=features)
    print(f"---> analyze_pros after format: \n{analyze_pros_result}")
    return analyze_pros_result


# 分析缺点
def analyze_cons(features):
    cons_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个产品评估专家"),
        ("human", "给定以下特点： {features}，列举出其中的缺点")
    ])
    return cons_template.format_prompt(features=features)


# 优缺点合并成最终的评估
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"


pros_branch_chain = (
    RunnableLambda(lambda x: analyze_pros(x)) | model | StrOutputParser()
)

cons_branch_chain = (
    RunnableLambda(lambda x: analyze_cons(x)) | model | StrOutputParser()
)

chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)

result = chain.invoke({"product_name": "MacBook Pro"})

print(result)