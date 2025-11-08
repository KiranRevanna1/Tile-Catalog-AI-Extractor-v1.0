from ultralytics import YOLO
import os

def detect_tiles(image_paths, output_dir="output/detections", conf_threshold=0.5):
    """
    Runs YOLO object detection on a list of images.
    Returns a list of detection result objects with crop paths and confidence scores.
    """

    os.makedirs(output_dir, exist_ok=True)

    print(f"[INFO] Loading YOLO model (yolov8s.pt)...")
    model = YOLO("yolov8s.pt")  # Pretrained on COCO, good for general objects

    detections = []

    for img_path in image_paths:
        print(f"[INFO] Detecting objects in {img_path} ...")
        results = model.predict(source=img_path, conf=conf_threshold, save=False)

        for r_idx, result in enumerate(results):
            boxes = result.boxes
            if boxes is None or len(boxes) == 0:
                print(f"  [WARN] No objects detected in {img_path}")
                continue

            for i, box in enumerate(boxes):
                cls_name = model.names[int(box.cls)]
                conf = float(box.conf)

                # Confidence filter
                if conf < conf_threshold:
                    continue

                # Crop the detection region
                crop_path = os.path.join(
                    output_dir, f"{os.path.basename(img_path).split('.')[0]}_{i}_{cls_name}.png"
                )
                result.save_crop(output_dir, file_name=os.path.basename(crop_path))

                detections.append({
                    "source": img_path,
                    "class": cls_name,
                    "confidence": conf,
                    "crop_path": crop_path
                })

                print(f"  [OK] Detected {cls_name} ({conf:.2f}) → {crop_path}")

    print(f"[SUCCESS] YOLO detected {len(detections)} objects across {len(image_paths)} pages.\n")
    return detections
