import fitz  # PyMuPDF
import os, re
from PIL import Image
import easyocr
from .yolo_detector import detect_tiles

# Initialize EasyOCR
reader = easyocr.Reader(["en"], gpu=False)

# Output folders
PAGE_DIR = "output/pages"
CROP_DIR = "output/crops"
os.makedirs(PAGE_DIR, exist_ok=True)
os.makedirs(CROP_DIR, exist_ok=True)


def extract_pdf_data(file_bytes, filename):
    """
    Extract product info (images + text) from an image-based PDF using YOLO for detection + OCR for text.
    """

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    all_products = []

    for page_num, page in enumerate(doc):
        print(f"[PROCESSING] Page {page_num + 1}/{len(doc)}")

        # Convert PDF page to an image
        pix = page.get_pixmap(dpi=300)
        page_path = os.path.join(PAGE_DIR, f"page_{page_num + 1}.png")
        pix.save(page_path)

        # YOLO detection for tile-like products
        cropped_imgs = detect_tiles(page_path, output_dir=CROP_DIR)
        print(f" - Found {len(cropped_imgs)} potential product tiles")

        # OCR + text extraction
        for img_path in cropped_imgs:
            results = reader.readtext(img_path, detail=1)
            if not results:
                continue

            # Filter by confidence >= 0.6
            filtered_text = [text for (_, text, conf) in results if conf >= 0.6]
            if not filtered_text:
                continue

            text_joined = " ".join(filtered_text)

            # Extract dimensions (e.g., "600x1200" or "300 × 600 mm")
            dims = None
            m = re.search(r"\b\d{2,4}\s*[x×]\s*\d{2,4}\b", text_joined)
            if m:
                dims = m.group(0)

            # Product name (first few words)
            name = filtered_text[0].strip() if filtered_text else "Unknown"

            # Create a product object
            all_products.append({
                "page": page_num + 1,
                "name": name,
                "dimensions": dims,
                "text": text_joined,
                "image_path": img_path,
                "confidence_avg": round(sum(conf for (_, _, conf) in results) / len(results), 3),
            })

    print(f"[DONE] Extracted {len(all_products)} products from {len(doc)} pages.")
    return {"file": filename, "products": all_products}
