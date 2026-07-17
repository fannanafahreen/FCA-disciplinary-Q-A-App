import os
from pypdf import PdfReader

data_folder = "data"
output_folder = "extracted_text"
os.makedirs(output_folder, exist_ok=True)

pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(data_folder, pdf_file)

    try:
        reader = PdfReader(pdf_path)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        # Save extracted text as a .txt file with the same name
        txt_filename = pdf_file.replace(".pdf", ".txt")
        txt_path = os.path.join(output_folder, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"✅ Extracted: {pdf_file} → {txt_filename} ({len(full_text)} characters)")

    except Exception as e:
        print(f"❌ Failed: {pdf_file} — {e}")

print("\nDone! Check the 'extracted_text' folder.")