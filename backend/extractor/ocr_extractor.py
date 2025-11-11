import os
import easyocr
from core.logger import get_logger

logger = get_logger(__name__)

reader = easyocr.Reader(["en"], gpu=False)

def extract_text_from_crops(detections, output_dir="output/ocr"):
    """
    Runs OCR on YOLO-detected crops.
    Returns a list with OCR results (text + confidence).
    """
    os.makedirs(output_dir, exist_ok=True)
    ocr_results = []

    for det in detections:
        crop_path = det.get("crop_path")
        if not os.path.exists(crop_path):
            continue

        logger.info(f"OCR on {crop_path}")
        results = reader.readtext(crop_path, detail=1)
        texts, total_conf = [], 0

        for (_, text, conf) in results:
            if conf >= 0.6:
                texts.append(text.strip())
                total_conf += conf

        if texts:
            combined_text = " ".join(texts)
            avg_conf = round(total_conf / len(texts), 3)

            ocr_result = {
                "page": det.get("page"),
                "crop_path": crop_path,
                "bbox": det.get("bbox"),
                "text": combined_text,
                "confidence": avg_conf
            }
            ocr_results.append(ocr_result)

    logger.info(f"OCR completed for {len(ocr_results)} crops")
    return ocr_results
