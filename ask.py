import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

# Load our search tools
print("Loading model and index...")
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")

with open("chunks_store.pkl", "rb") as f:
    chunks = pickle.load(f)

def search(query, k=3):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k)
    results = [chunks[idx] for idx in indices[0]]
    return results

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

if __name__ == "__main__":
    print("\n Ask My Documents — FCA Final Notices RAG\n(type 'quit' to exit)\n")
    while True:
        question = input("Your question: ")
        if question.lower() in ["quit", "exit"]:
            break
        answer = ask(question)
        print(f"\n{answer}\n")
        print("-" * 50)