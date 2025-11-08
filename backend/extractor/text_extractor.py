import easyocr
import re

# Initialize the OCR reader (CPU only; GPU=False ensures stability)
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path, min_conf=0.5):
    """
    Extracts readable text from an image and filters low-confidence results.
    """
    results = reader.readtext(image_path, detail=1)
    
    filtered_texts = [text for (_, text, conf) in results if conf >= min_conf]
    joined_text = " ".join(filtered_texts)
    
    return joined_text.strip()

def parse_product_details(text):
    """
    Parses text to extract product name, dimensions, and specifications.
    Example:
        'TileX 600x1200 Glossy Finish' ->
            name='TileX'
            dimensions='600x1200'
            specs='Glossy Finish'
    """
    # Extract dimensions (e.g., 600x1200, 300×600, etc.)
    dims_match = re.search(r"\b\d{2,4}\s*[x×]\s*\d{2,4}\b", text)
    dimensions = dims_match.group(0) if dims_match else None

    # Split text for possible name/spec extraction
    words = text.split()
    name = words[0] if words else "Unknown"
    specs = " ".join(words[1:]) if len(words) > 1 else None

    return {
        "name": name,
        "dimensions": dimensions,
        "specifications": specs,
        "raw_text": text
    }
