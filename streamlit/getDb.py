import time
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores.neo4j_vector import Neo4jVector

### Embeddings
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
### Get data
vectordb = Chroma(persist_directory = "../data/Chroma/", collection_name= "Harry_Potter", embedding_function = embeddings)
vector_index = Neo4jVector.from_existing_graph(
    embeddings,
    url=st.secrets.Neo4j["url"],
    username=st.secrets.Neo4j["username"],
    password=st.secrets.Neo4j["password"],
    index_name='persons',
    node_label=["Person", 'Location', 'Skill', 'Organization', 'Award', "Country", 'Religion' ],
    text_node_properties=['name', "positionHeld", "causeOfDeath", "dateOfBirth", "numberOfChildren", "academicDegree", "dateOfDeath", "age", "productType", "foundingDate" ],
    embedding_node_property='embedding',
)

llm = ChatOllama(model="llama3")

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use five sentences maximum. Keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 

{context}

Question: {question}

Helpful Answer:
"""
prompt = PromptTemplate.from_template(template)

vector_qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_index.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt})

def ask_question(question):
    result = chain.invoke({"query": question, "context": vector_qa.invoke(question)})
    return result["result"]