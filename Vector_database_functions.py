from langchain.vectorstores import Chroma
import chromadb
from chromadb.config import Settings

#chroma_client = chromadb.HttpClient(settings=Settings(allow_reset=True))


#Creates new collection and adds documents to it
def Create(docs, collection_name, embedding_function, data_directory):
    #document_collection = chroma_client.create_collection(name=collection_name)
    ids = [str(i) for i in range(1, len(docs) + 1)]
    #db = Chroma(client=chroma_client, collection_name=collection_name, persist_directory=data_directory, embedding_function=embedding_function)
    Chroma.from_documents(docs, embedding_function, collection_name=collection_name, persist_directory=data_directory)
    #return "Database created and populated with " + str(document_collection.count()) + " documents"

### Adds documents to an existing collection
def Add_docs(doc, collection_name, embedding_function, data_directory):
    db = get_db(collection_name, data_directory, embedding_function)
    db.add_documents(doc)

### Get the whole database
def get_db(collection_name, data_directory, embedding_function):
    db = Chroma(persist_directory = data_directory, collection_name=collection_name, embedding_function = embedding_function)
    return db

def update(id, doc, collection_name, data_directory, embedding_function):
   db = get_db(collection_name, data_directory, embedding_function)
   db.update_document(id, doc)
   return "Document updated"

def delete(id, collection_name, data_directory, embedding_function):
   db = get_db(collection_name, data_directory, embedding_function)
   db.delete(id)
   return "Document deleted"

def delete_last_index(collection_name, data_directory, embedding_function):
   db = get_db(collection_name, data_directory, embedding_function)
   db.delete(ids=[str(len(db)-1)])
   return "Document deleted"

### Deletes the whole collection
#def Delete_Collection(collection_name):
 #   chroma_client.delete_collection(name=collection_name)
  #  return "Collection deleted"
