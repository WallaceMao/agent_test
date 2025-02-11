import hashlib
import os
import chromadb
import re
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from zhipuai import ZhipuAI
from dotenv import load_dotenv


load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "db", "chroma_db")
db_client = chromadb.PersistentClient(path=persistent_dir)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def handle_chroma():
    db_client.list_collections()
    # count = client.count_collections()
    # print(count)
    # collection = client.get_collection("langchain")
    # print(f"===> item count: {collection.count()}")
    # first_result = collection.peek(1)
    # print(first_result)
    # print(first_result.get("documents"))


def test_split():
    text = "LangChain: A Framework for LLM-Powered Applications"
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=0)
    text_list = text_splitter.split_text(text)
    print(text_list)
    # separator = "\\\n"
    # re_text_list = re.split(separator, text)
    # print()


def zhipu_ai():
    client = ZhipuAI()
    resp = client.embeddings.create(
        model="embedding-3",
        input=[
            "美食非常美味，服务员也很友好。",
            "这部电影既刺激又令人兴奋。",
            "阅读书籍是扩展知识的好方法。"
        ],
    )
    print(resp)


def embed_model():
    EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    EMBED_MODEL.encode()


def hash_test():
    text = "万万万"
    print(text.encode())
    print(hashlib.md5(text.encode()))
    print(hashlib.md5(text.encode()).hexdigest())


if __name__ == "__main__":
    collections = db_client.list_collections()
    print(collections)
    langchain_collection = db_client.get_collection("langchain_test")
    ids = langchain_collection.get()["ids"]
    print(f"ids in langchain_test: {ids}")
    first_doc = langchain_collection.get(ids='demo_0_0')
    print(f"first_doc: {first_doc}")
