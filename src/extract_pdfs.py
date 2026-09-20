from pathlib import Path
from pypdf import PdfReader

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

for pdf_file in RAW_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_file)

    text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        text += f"\n\n--- PAGE {page_number} ---\n\n"
        text += page_text

    output_file = PROCESSED_DIR / f"{pdf_file.stem}.txt"
    output_file.write_text(text, encoding="utf-8")

    print(f"Processed: {pdf_file.name}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Characters: {len(text)}")
    print("-" * 70)

print("PDF extraction completed.")