import re
import os

def structure_products(ocr_results, output_dir="output/structured"):
    """
    Convert OCR outputs into structured product info.
    Groups text by page and infers product name, dimensions, specs, and image path.
    """

    os.makedirs(output_dir, exist_ok=True)
    structured_products = []

    for item in ocr_results:
        text = item["text"]
        img_path = item["crop_path"]

        # --- Extract product name ---
        # Heuristic: first 3 words with capital letters or distinctive words
        name_match = re.search(r"([A-Z][A-Za-z0-9\- ]{2,})", text)
        name = name_match.group(1).strip() if name_match else "Unknown Product"

        # --- Extract dimensions ---
        # Common formats: 600x1200, 300 × 600 mm, 800 x 800mm
        dim_match = re.search(r"\b\d{2,4}\s*[x×]\s*\d{2,4}\s*(mm|MM)?\b", text)
        dimensions = dim_match.group(0) if dim_match else "Unknown"

        # --- Extract specifications ---
        specs = extract_specs(text)

        structured_products.append({
            "page": item["page"],
            "name": name,
            "dimensions": dimensions,
            "specifications": specs,
            "image_path": img_path,
            "confidence": item["confidence"],
        })

    # --- Save JSON output for inspection ---
    out_json = os.path.join(output_dir, "structured_products.json")
    import json
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(structured_products, f, indent=2)

    print(f"✅ Structured {len(structured_products)} products saved to {out_json}")
    return structured_products


def extract_specs(text):
    """
    Extract key-value style specifications from OCR text.
    Example:
      "Finish: Glossy | Size: 600x1200 | Material: Ceramic"
    """
    specs = {}

    # Normalize text
    text = text.replace("|", "\n").replace("•", "\n").replace(":", ": ")
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 3]

    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            specs[key.strip()] = val.strip()

    # Common attributes (fallbacks)
    if "Finish" not in specs and re.search(r"matt|gloss|polished", text, re.I):
        specs["Finish"] = re.findall(r"(matt|glossy|polished)", text, re.I)[0]

    return specs
