import os
from extractor.pdf_to_images import pdf_to_images
from extractor.yolo_detector import detect_tiles
from extractor.ocr_extractor import extract_text_from_crops
from extractor.formatter import structure_products

def process_pdf(pdf_path, output_dir="output"):
    """
    Complete pipeline:
    PDF → Pages → YOLO Detection → OCR → Structured JSON
    """
    pages_dir = os.path.join(output_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    print("Step 1: Convert PDF to images...")
    pages = pdf_to_images(pdf_path, output_dir=pages_dir)

    print("Step 2: Detect tiles using YOLO...")
    detections = detect_tiles(pages, output_dir=os.path.join(output_dir, "detections"))

    print("Step 3: Extract text using EasyOCR...")
    ocr_results = extract_text_from_crops(detections, output_dir=os.path.join(output_dir, "ocr"))

    print("Step 4: Structure data...")
    structured = structure_products(ocr_results, output_dir=os.path.join(output_dir, "structured"))

    print("Pipeline complete.")
    return {
        "pages": pages,
        "detections": detections,
        "ocr": ocr_results,
        "structured": structured
    }
