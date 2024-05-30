from langchain.vectorstores import Chroma

def get(embedding_function, data_directory):
    db = Chroma(persist_directory = data_directory, embedding_function = embedding_function)
    print(db.get().keys())
    print(len(db.get()["ids"]))
    return db