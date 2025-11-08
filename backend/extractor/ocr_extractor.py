import os
import easyocr
from PIL import Image

reader = easyocr.Reader(["en"], gpu=False)

def extract_text_from_crops(detections, output_dir="output/ocr"):
    """
    Runs OCR on YOLO-detected product crops.
    Returns a structured list with OCR text + confidence for each crop.
    """
    os.makedirs(output_dir, exist_ok=True)
    ocr_results = []

    for det in detections:
        crop_path = det.get("crop_path")
        if not crop_path or not os.path.exists(crop_path):
            continue

        print(f"🔍 Running OCR on: {crop_path}")
        results = reader.readtext(crop_path, detail=1)

        text_items = []
        total_conf = 0.0

        for (bbox, text, conf) in results:
            if conf < 0.6:  
                continue
            text_items.append(text.strip())
            total_conf += conf

        if not text_items:
            continue

        avg_conf = round(total_conf / len(text_items), 3)
        text_combined = " ".join(text_items)

        ocr_result = {
            "crop_path": crop_path,
            "page": det.get("page"),
            "bbox": det.get("bbox"),
            "text": text_combined,
            "confidence": avg_conf
        }

        ocr_results.append(ocr_result)

        txt_path = os.path.join(output_dir, f"{os.path.basename(crop_path)}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text_combined)

    return ocr_results
