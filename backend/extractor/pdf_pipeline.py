import os
from extractor.pdf_to_images import pdf_to_images
from extractor.yolo_detector import detect_tiles
from extractor.ocr_extractor import extract_text_from_crops

def process_pdf(pdf_path, output_dir="output"):
    """
    Full PDF → Images → YOLO detection → OCR pipeline.
    Returns structured data for all detected tiles/products.
    """

    pages_dir = os.path.join(output_dir, "pages")
    detections_dir = os.path.join(output_dir, "detections")
    ocr_dir = os.path.join(output_dir, "ocr")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(detections_dir, exist_ok=True)
    os.makedirs(ocr_dir, exist_ok=True)

    print("\n Converting PDF to Images...")
    page_images = pdf_to_images(pdf_path, output_dir=pages_dir)

    print("\n Detecting Objects (YOLO)...")
    detections = detect_tiles(page_images, output_dir=detections_dir, conf_threshold=0.5)

    print("\n Extracting Text via OCR (EasyOCR)...")
    ocr_results = extract_text_from_crops(detections, output_dir=ocr_dir)

    print("\n PDF processing complete.\n")

    return {
        "pdf_path": pdf_path,
        "pages": page_images,
        "detections": detections,
        "ocr": ocr_results
    }