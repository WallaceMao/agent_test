import os
import chromadb


current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "db", "chroma_db")
client = chromadb.PersistentClient(path=persistent_dir)

collection = client.get_collection("langchain")
print(collection.peek(1).popitem())
