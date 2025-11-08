import os
from ultralytics import YOLO

def retrain_model():
    model = YOLO("backend/training/model/yolov8s_custom.pt")

    data_yaml = """
    path: backend/training/datasets
    train: images
    val: images
    names:
      0: tile
    """

    with open("backend/training/datasets/data.yaml", "w") as f:
        f.write(data_yaml)

    model.train(
        data="backend/training/datasets/data.yaml",
        epochs=5,
        imgsz=640,
        project="backend/training/runs",
        name="autotrain",
        exist_ok=True,
    )

if __name__ == "__main__":
    retrain_model()
