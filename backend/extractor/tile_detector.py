from ultralytics import YOLO
import os

# Load the best custom model
MODEL_PATH = os.path.join("runs", "detect", "train", "weights", "best.pt")

# Fallback to pre-trained if custom one doesn’t exist yet
model = YOLO(MODEL_PATH if os.path.exists(MODEL_PATH) else "yolov8s.pt")

def detect_tiles(image_path, confidence=0.5):
    results = model.predict(source=image_path, conf=confidence)
    detections = []
    
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist(),
                "label": model.names[int(box.cls)]
            })
    return detections
