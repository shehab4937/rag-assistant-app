from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path("data/raw")

for pdf_file in DATA_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text

    print("=" * 70)
    print(f"File: {pdf_file.name}")
    print(f"Pages: {len(reader.pages)}")
    print(f"Characters extracted: {len(text)}")

    if len(text.strip()) > 100:
        print("Status: TEXT EXTRACTABLE")
    else:
        print("Status: POSSIBLY SCANNED / OCR NEEDED")