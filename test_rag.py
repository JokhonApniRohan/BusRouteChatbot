from dotenv import load_dotenv
import os

load_dotenv()

hf_token = os.getenv("GROQ_API_KEY")
if not hf_token:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

from rag_pipeline.loader import load_and_split_documents
from rag_pipeline.embedder import create_vector_store
from rag_pipeline.rag import build_qa_chain

def main():
    docs = load_and_split_documents("data/bus_routes.md")
    vector_store = create_vector_store(docs)
    qa_chain = build_qa_chain(vector_store)
    query = input('Enter your query: ')
    answer = qa_chain.run(query)
    print("Q:", query)
    print("A:", answer)

while True:
    if __name__ == "__main__":
        main()
