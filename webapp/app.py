from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

from rag_pipeline.loader import load_and_split_documents
from rag_pipeline.embedder import create_vector_store
from rag_pipeline.rag import build_qa_chain

load_dotenv()  # Load environment variables from .env

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

# Load data once on startup
docs = load_and_split_documents("data/bus_routes.md")
vector_store = create_vector_store(docs)

# Get HuggingFace Hub API token from environment variables
huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if huggingface_token is None:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not set in environment")

# Build the QA chain with the token passed in
qa_chain = build_qa_chain(vector_store, huggingfacehub_api_token=huggingface_token)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query")
    answer = qa_chain.run(query)
    return {"answer": answer}
