from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq


import os

def build_qa_chain(vector_store):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",  # Or llama3-70b-8192 if needed
        api_key=os.getenv("GROQ_API_KEY"),  # Use environment variable
        temperature=0.5
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
    return qa_chain

