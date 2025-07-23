from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag_pipeline.loader import load_and_split_documents
from rag_pipeline.embedder import create_vector_store
from rag_pipeline.rag import build_qa_chain



load_dotenv()  # ✅ Loads .env values like GROQ_API_KEY

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

# Load data once on startup
docs = load_and_split_documents("data/bus_routes.md")
vector_store = create_vector_store(docs)

# ✅ Check for GROQ API key from env
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is not set in .env file")

# Build QA chain using the vector store
qa_chain = build_qa_chain(vector_store)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query")
    answer = qa_chain.run(query)
    return {"answer": answer}
