from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# template = "给我将一个关于{topic}的笑话"
# prompt_template = ChatPromptTemplate.from_template(template)
#
# print("======== Prompt from template ========")
# prompt = prompt_template.invoke({"topic": "猫"})
# print(prompt)
#
# template_multiple = """
# 你是一个有用的助手。
# 人类： 给我将一个{adjective}的关于{animal}故事
# 助手："""
#
# prompt_multiple = ChatPromptTemplate.from_template(template_multiple)
# prompt = prompt_multiple.invoke({"adjective": "恐怖", "animal": "狗"})
# print("======== Prompt from multiple template ========")
# print(prompt)
#
# messages = [
#     ("system", "你是一个会将关于{topic}的故事的喜剧演员"),
#     ("human", "给我将{joke_count}个笑话")
# ]
# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic": "律师", "joke_count": 2})
# print("======== Prompt from Human and System message ========")
# print(prompt)

pros_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个产品评估专家"),
    ("human", "给定以下特点： {features}，列举出其中的优点")
])
print(pros_template.format_prompt(features="aaabbbccc"))
