from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import ollama

app = FastAPI()

# Load everything once when the server starts
print("Loading model and index...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
index = faiss.read_index("faiss_index.bin")

with open("chunks_store.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Ready!")

class Question(BaseModel):
    question: str

def search(query, k=3):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k)
    return [chunks[idx] for idx in indices[0]]

def ask(question):
    relevant_chunks = search(question, k=3)

    context = ""
    for i, chunk in enumerate(relevant_chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"

    prompt = f"""You are a compliance research assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't have enough information.
Always mention which source(s) your answer came from.

Context:
{context}

Question: {question}

Answer:"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

@app.post("/ask")
def ask_endpoint(q: Question):
    answer = ask(q.question)
    return {"answer": answer}

@app.get("/")
def serve_homepage():
    return FileResponse("index.html")