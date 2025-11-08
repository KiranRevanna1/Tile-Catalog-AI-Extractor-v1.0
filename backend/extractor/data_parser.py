def parse_product_data(ocr_results, image_paths):
    """
    Combines OCR text + image data into a structured format.
    """
    products = []
    for i, (ocr, img) in enumerate(zip(ocr_results, image_paths)):
        products.append({
            "id": i + 1,
            "name": ocr["name"],
            "dimensions": ocr["dimensions"],
            "text": ocr["text"],
            "image_path": img
        })
    return products
