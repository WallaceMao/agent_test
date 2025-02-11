import hashlib
import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from sentence_transformers import SentenceTransformer
import chromadb
"""
不使用 openAI等在线模型，只使用 chromadb 和 sentence_transformers (SBERT) 来本地实现
"""
file_name = "odyssey.txt"
current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "books", "odyssey.txt")
file_path = os.path.join(current_dir, "books", file_name)
persistent_dir = os.path.join(current_dir, "db", "chroma_db")

load_dotenv()
embedding_model = os.environ.get("DEFAULT_EMBEDDING_MODEL")
embedding_collection_name = "langchain_test"
embedding_prefix = "odyssey_"

# ai client
# ai_client = ZhipuAI()

# embedding
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# 向量数据库
db_client = chromadb.PersistentClient(path=persistent_dir)
embedding_collection = db_client.get_or_create_collection(embedding_collection_name)

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"文件 {file_path} 不存在"
    )

# 读取文件
loader = TextLoader(file_path, encoding="utf8")
documents = loader.load()

# 切分文件
# 注意 chunk_size 和 chunk_overlap 两个参数
# 要使用 RecursiveCharacterTextSplitter 才能正常切分
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print("\n---- 文件Chunk信息----\n")
print(f"chunks数量： {len(docs)}\n")

# 对docs进行分片，防止单次数量过大导致调用大模型接口失败
batch_size = 64
batch_list = list(docs[i:i+batch_size] for i in range(0, len(docs), batch_size))
print(f"chunks的批次的数量： {len(batch_list)}\n")

# 删除掉原有的embedding
existing_ids = embedding_collection.get()["ids"]
rag_ids = [doc_id for doc_id in existing_ids if doc_id.startswith(embedding_prefix)]
if rag_ids:
    embedding_collection.delete(ids=rag_ids)

# 计算embedding
for batch_num in range(0, len(batch_list)):
    batch_documents = batch_list[batch_num]
    text_list = [i.page_content for i in batch_documents]
    batch_prefix = f"{embedding_prefix}{batch_num}_"
    ids = [f"{batch_prefix}{i}" for i in range(0, len(text_list))]
    meta_datas = [{"source": file_name, "content_hash": hashlib.md5(text.encode()).hexdigest()[:8]} for text in text_list]
    embeddings = EMBED_MODEL.encode(text_list)
    embedding_collection.add(ids=ids, embeddings=embeddings, documents=text_list, metadatas=meta_datas)

    # resp = ai_client.embeddings.create(
    #     model=embedding_model,
    #     input=text_list,
    # )
    # embedding_collection.add(ids=, embeddings=, documents=, metadatas=)


# if not os.path.exists(persistent_dir):
#     print("存储目录不存在，开始初始化向量数据库")
#

    # # 创建embedding
    # embeddings = OpenAIEmbeddings(model=embedding_model)
    # # embeddings = ZhipuAIEmbeddings(model=embedding_model)
    #
    # # 对docs进行分片，防止单次数量过大导致调用大模型接口失败
    # batch_size = 1
    # chunks_list = list(docs[i:i+batch_size] for i in range(0, len(docs), batch_size))
    # print(f"批量chunks_list的数量： {len(chunks_list)}")
    #
    # # 创建向量数据库
    # vectorstore = Chroma(collection_name="langchain", embedding_function=embeddings,
    #                      persist_directory=persistent_dir)
    # for chunk in docs:
    #     print(f"====> size of doc: {len([chunk])}")
    #     vectorstore.add_documents([chunk])

    # # 智谱AI 创建embedding
    # zhipu_client = ZhipuAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # for chunk in chunks_list:
    #     zhipu_resp = zhipu_client.embeddings.create(
    #         model=embedding_model,
    #         input=chunk
    #     )
#
#     print("\n 创建向量数据库完成")
#
# else:
#     print("向量数据库已经存在")
