import os
from ultralytics import YOLO
from PIL import Image
from core.logger import get_logger

logger = get_logger(__name__)

# Load YOLO model (ensure you have a weights file in models/)
MODEL_PATH = "runs/detect/train15/weights/best.pt"

if not os.path.exists(MODEL_PATH):
    logger.warning(f"[WARN] YOLO model not found at {MODEL_PATH}. Detection will be skipped.")
    model = None
else:
    model = YOLO(MODEL_PATH)


def detect_tiles(input_data, output_dir="output/detections", conf_threshold=0.5):
    """
    Runs YOLO detection on one or multiple image paths.
    Returns a list of detected tile crops with bounding boxes.
    """

    os.makedirs(output_dir, exist_ok=True)

    if model is None:
        logger.error("YOLO model is not loaded. Please place 'tile_detector.pt' in the models folder.")
        return []

    # Handle both single image and list of images
    if isinstance(input_data, str):
        input_images = [input_data]
    else:
        input_images = input_data

    detections = []

    for img_path in input_images:
        if not os.path.exists(img_path):
            logger.warning(f"Image not found: {img_path}")
            continue

        logger.info(f"Running YOLO detection on: {img_path}")
        results = model(img_path, conf=conf_threshold)

        if not results or not results[0].boxes:
            logger.info(f"No detections found for {img_path}")
            continue

        img = Image.open(img_path)
        img_name = os.path.splitext(os.path.basename(img_path))[0]

        for i, box in enumerate(results[0].boxes):
            coords = box.xyxy[0].cpu().numpy().tolist()
            conf = float(box.conf[0].cpu().numpy())

            x1, y1, x2, y2 = map(int, coords)
            crop = img.crop((x1, y1, x2, y2))

            crop_path = os.path.join(output_dir, f"{img_name}_det_{i+1}.png")
            crop.save(crop_path)

            detections.append({
                "page": img_name,
                "bbox": [x1, y1, x2, y2],
                "confidence": conf,
                "crop_path": crop_path
            })

        logger.info(f"✅ {len(results[0].boxes)} objects detected in {img_name}")

    return detections
