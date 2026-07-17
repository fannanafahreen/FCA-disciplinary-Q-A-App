import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load our chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Load a free local embedding model (downloads once, ~80MB)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Turn each chunk's text into an embedding
texts = [chunk["text"] for chunk in chunks]
print("Generating embeddings... (this may take a minute)")
embeddings = model.encode(texts, show_progress_bar=True)

# Build a FAISS index (a searchable database of these vectors)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save the FAISS index to disk
faiss.write_index(index, "faiss_index.bin")

# Save the chunks too, so we can map search results back to real text
with open("chunks_store.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"\n✅ Done! Indexed {len(chunks)} chunks.")
print("Saved: faiss_index.bin and chunks_store.pkl")