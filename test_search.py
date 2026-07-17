from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

# Load everything we built
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")

with open("chunks_store.pkl", "rb") as f:
    chunks = pickle.load(f)

# Try a test question
query = "Which firms were fined for anti-money laundering failures?"

query_embedding = model.encode([query]).astype("float32")

# Search top 3 most relevant chunks
k = 3
distances, indices = index.search(query_embedding, k)

print(f"Query: {query}\n")
for rank, idx in enumerate(indices[0]):
    chunk = chunks[idx]
    print(f"--- Result {rank+1} (source: {chunk['source']}) ---")
    print(chunk["text"][:300], "...\n")