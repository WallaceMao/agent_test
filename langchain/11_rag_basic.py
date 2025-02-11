import os

from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import ZhipuAIEmbeddings


current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "books", "odyssey.txt")
file_path = os.path.join(current_dir, "books", "langchain_demo.txt")
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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    print("\n---- 文件Chunk信息----\n")
    print(f"chunks数量： {len(docs)}")

    # 创建embedding
    embeddings = OpenAIEmbeddings(model=embedding_model)
    # embeddings = ZhipuAIEmbeddings(model=embedding_model)

    # 对docs进行分片，防止单次数量过大导致调用大模型接口失败
    batch_size = 1
    chunks_list = list(docs[i:i+batch_size] for i in range(0, len(docs), batch_size))
    print(f"批量chunks_list的数量： {len(chunks_list)}")

    # 创建向量数据库
    vectorstore = Chroma(collection_name="langchain", embedding_function=embeddings,
                         persist_directory=persistent_dir)
    for chunk in docs:
        print(f"====> size of doc: {len([chunk])}")
        vectorstore.add_documents([chunk])

    # # 智谱AI 创建embedding
    # zhipu_client = ZhipuAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # for chunk in chunks_list:
    #     zhipu_resp = zhipu_client.embeddings.create(
    #         model=embedding_model,
    #         input=chunk
    #     )

    print("\n 创建向量数据库完成")

else:
    print("向量数据库已经存在")
