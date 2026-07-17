import os
import json

input_folder = "extracted_text"
output_file = "chunks.json"

chunk_size = 500       # words per chunk
chunk_overlap = 50     # words shared between consecutive chunks

def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

all_chunks = []

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text, chunk_size, chunk_overlap)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": filename,
                "chunk_id": i,
                "text": chunk
            })

        print(f"✅ {filename} → {len(chunks)} chunks")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)

print(f"\nDone! {len(all_chunks)} total chunks saved to {output_file}")