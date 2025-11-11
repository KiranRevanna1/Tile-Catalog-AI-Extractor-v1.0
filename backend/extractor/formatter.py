import os, re, json
from core.logger import get_logger

logger = get_logger(__name__)

def structure_products(ocr_results, output_dir="output/structured"):
    """
    Converts OCR outputs into structured product information.
    """
    os.makedirs(output_dir, exist_ok=True)
    structured = []

    for item in ocr_results:
        text = item["text"]
        img_path = item["crop_path"]

        name = _extract_name(text)
        dimensions = _extract_dimensions(text)
        specs = _extract_specs(text)

        structured.append({
            "page": item["page"],
            "name": name,
            "dimensions": dimensions,
            "specifications": specs,
            "image_path": img_path,
            "confidence": item["confidence"],
        })

    path = os.path.join(output_dir, "structured_products.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)

    logger.info(f"Structured {len(structured)} products saved → {path}")
    return structured


def _extract_name(text):
    m = re.search(r"([A-Z][A-Za-z0-9\- ]{2,})", text)
    return m.group(1).strip() if m else "Unknown Product"

def _extract_dimensions(text):
    m = re.search(r"\b\d{2,4}\s*[x×]\s*\d{2,4}\s*(mm|MM)?\b", text)
    return m.group(0) if m else "Unknown"

def _extract_specs(text):
    specs = {}
    text = text.replace("|", "\n").replace("•", "\n")
    for line in [l.strip() for l in text.split("\n") if ":" in l]:
        k, v = line.split(":", 1)
        specs[k.strip()] = v.strip()
    return specs
