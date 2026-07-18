from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import faiss
import pickle
import json
import boto3
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load everything once when the server starts
print("Loading model and index...")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
index = faiss.read_index("faiss_index.bin")

with open("chunks_store.pkl", "rb") as f:
    chunks = pickle.load(f)

# Bedrock client - pointed at us-east-1 (N. Virginia), where Nova Lite access was granted
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

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

    response = bedrock.converse(
        modelId="amazon.nova-2-lite-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        inferenceConfig={"maxTokens": 500}
    )

    answer = response["output"]["message"]["content"][0]["text"]
    return answer

@app.post("/ask")
def ask_endpoint(q: Question):
    answer = ask(q.question)
    return {"answer": answer}

@app.get("/")
def serve_homepage():
    return FileResponse("index.html")