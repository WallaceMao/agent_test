import os
import chromadb

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


# current_dir = os.path.dirname(os.path.abspath(__file__))
# persistent_dir = os.path.join(current_dir, "db", "chroma_db")
# client = chromadb.PersistentClient(path=persistent_dir)

# collection = client.get_collection("langchain")
# print(collection.peek(1).popitem())

if __name__ == "__main__":
    lst = [1,2,3,4,5]
    c = chunks(lst, 3)
    print(list(c))
    print([lst[i:i+2]] for i in range(0, len(lst), 2))