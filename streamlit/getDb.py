
from langchain_community.vectorstores import Chroma # type: ignore
from langchain.callbacks.manager import CallbackManager # type: ignore
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # type: ignore
from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain_community.llms import Ollama # type: ignore
from langchain.chains import RetrievalQA # type: ignore
from langchain.prompts import PromptTemplate # type: ignore


model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

vectordb = ()

def get(embedding_function):
    db = Chroma(persist_directory = 'data/chroma/', embedding_function = embedding_function)
    return db


def getDb():
    vectordb = get(embeddings)

llm = Ollama(model="mistral", callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use five sentences maximum. Keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 

{context}

Question: {question}

Helpful Answer:
"""
def ask_question(question):
    vectordb = get(embeddings)
    prompt = PromptTemplate.from_template(template)
    chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt})
    return chain({"query": question})["result"]