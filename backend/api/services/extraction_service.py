import io
from extractor.pdf_parser import extract_pdf_data

def process_uploaded_pdf(file_bytes, filename):
    print(f"[INFO] Processing uploaded file: {filename}")
    result = extract_pdf_data(file_bytes, filename)
    return {"filename": filename, "products": result.get("products", [])}
