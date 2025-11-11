import os

def train_yolo():
    """
    Placeholder for YOLOv8 training command.
    You can use ultralytics library or CLI command here.
    """
    os.system("yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640")

if __name__ == "__main__":
    train_yolo()
