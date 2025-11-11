import fitz
import os
import re
import easyocr
from extractor.yolo_detector import detect_tiles
from core.config import PDF_DPI
from core.logger import get_logger

logger = get_logger(__name__)
reader = easyocr.Reader(["en"], gpu=False)

def extract_pdf_data(file_bytes, filename):
    """
    Process PDF bytes → extract product info using YOLO + OCR.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    PAGE_DIR = "output/pages"
    CROP_DIR = "output/crops"
    os.makedirs(PAGE_DIR, exist_ok=True)
    os.makedirs(CROP_DIR, exist_ok=True)

    all_products = []

    for page_num, page in enumerate(doc, start=1):
        logger.info(f"Processing page {page_num}/{len(doc)}")
        pix = page.get_pixmap(dpi=PDF_DPI)
        page_path = os.path.join(PAGE_DIR, f"page_{page_num}.png")
        pix.save(page_path)

        detections = detect_tiles(page_path, output_dir=CROP_DIR)

        for det in detections:
            img_path = det["crop_path"]
            results = reader.readtext(img_path, detail=1)
            if not results:
                continue

            filtered = [(t, c) for (_, t, c) in results if c >= 0.6]
            if not filtered:
                continue

            text = " ".join([t for (t, _) in filtered])
            conf = sum(c for (_, c) in filtered) / len(filtered)

            dim_match = re.search(r"\b\d{2,4}\s*[x×]\s*\d{2,4}\b", text)
            dims = dim_match.group(0) if dim_match else "Unknown"
            name = text.split(" ")[0] if text else "Unknown"

            all_products.append({
                "page": page_num,
                "name": name,
                "dimensions": dims,
                "text": text,
                "image_path": img_path,
                "confidence_avg": round(conf, 3),
            })

    doc.close()
    logger.info(f"Extracted {len(all_products)} products.")
    return {"file": filename, "products": all_products}
