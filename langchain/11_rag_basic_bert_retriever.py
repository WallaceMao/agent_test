import os

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "db", "chroma_db")
db_client = chromadb.PersistentClient(path=persistent_dir)
embedding_model = os.environ.get("DEFAULT_EMBEDDING_MODEL")
embedding_collection_name = "langchain_test"
embedding_prefix = "odyssey_"
embedding_collection = db_client.get_collection(embedding_collection_name)
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# 问题
query = "Who is Odysseus' wife?"
query_embedding = EMBED_MODEL.encode(query).tolist()

results = embedding_collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

context = "\n".join(results['documents'][0])

print(context)

model = ChatOpenAI(model=os.environ.get("DEFAULT_MODEL"))
prompt_template = ChatPromptTemplate.from_template("""
基于以下上下文
{context}

问题： {question}
如果上下文中没有信息，请显示未查到数据。结果请用中文给出回答：
""")

chain = prompt_template | model | StrOutputParser()

response = chain.invoke({"context": context, "question": query})

print(f"结果： {response}")

