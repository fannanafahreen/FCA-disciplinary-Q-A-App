import os
import requests

# Create a folder to store the PDFs
os.makedirs("data", exist_ok=True)

# List of FCA Final Notice PDFs
pdf_urls = [
    "https://www.fca.org.uk/publication/final-notices/barclays-bank-uk-plc-2025.pdf",
    "https://www.fca.org.uk/publication/final-notices/nationwide-building-society-2025.pdf",
    "https://www.fca.org.uk/publication/final-notices/institute-certified-bookeepers-2025.pdf",
    "https://www.fca.org.uk/publication/final-notices/barclays-bank-plc-2025.pdf",
    "https://www.fca.org.uk/publication/final-notices/jean-noel-alba-2025.pdf",
    "https://www.fca.org.uk/publication/final-notices/final-notice-jpm.pdf",
    "https://www.fca.org.uk/publication/final-notices/pas.pdf",
    "https://www.fca.org.uk/publication/final-notices/fc-group-limited.pdf",
]

headers = {"User-Agent": "Mozilla/5.0"}  # some sites block requests without this

for url in pdf_urls:
    filename = url.split("/")[-1]
    filepath = os.path.join("data", filename)

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # error out if download failed

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✅ Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Failed: {filename} — {e}")

print("\nDone! Check the 'data' folder.")