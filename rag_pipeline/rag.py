from langchain.chains import RetrievalQA
from langchain_community.llms import Groq

import os

def build_qa_chain(vector_store):
    llm = Groq(
        model="llama3-8b-8192",  # Or llama3-70b-8192 if needed
        api_key=os.getenv("GROQ_API_KEY"),  # Use environment variable
        temperature=0.5,
        max_tokens=512,
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever())
    return qa_chain

