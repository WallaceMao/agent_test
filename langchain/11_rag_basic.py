import os

from dotenv import load_dotenv
from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "us_bill_of_rights.txt")
persistent_dir = os.path.join(current_dir, "db", "chroma_db")

load_dotenv()
embedding_model = os.environ.get("DEFAULT_EMBEDDING_MODEL")

if not os.path.exists(persistent_dir):
    print("存储目录不存在，开始初始化向量数据库")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"文件 {file_path} 不存在"
        )

    # 读取文件
    loader = TextLoader(file_path, encoding="utf8")
    documents = loader.load()

    # 切分文件
    # 注意 chunk_size 和 chunk_overlap 两个参数
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    print("\n---- 文件Chunk信息----\n")
    print(f"chunks数量： {len(docs)}")

    # 创建embedding
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 创建向量数据库
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_dir
    )
    print("\n 创建向量数据库完成")

else:
    print("向量数据库已经存在")
