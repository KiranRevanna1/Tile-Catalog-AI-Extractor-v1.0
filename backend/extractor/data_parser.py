def parse_product_data(ocr_results, image_paths):
    """
    Combines OCR + image paths into structured product records.
    """
    products = []
    for i, (ocr, img) in enumerate(zip(ocr_results, image_paths)):
        products.append({
            "id": i + 1,
            "name": ocr.get("name", "Unknown"),
            "dimensions": ocr.get("dimensions", "Unknown"),
            "text": ocr.get("text", ""),
            "image_path": img
        })
    return products
