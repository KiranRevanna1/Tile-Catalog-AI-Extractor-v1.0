import os
import shutil
from core.logger import get_logger

logger = get_logger(__name__)

def prepare_dataset(src_dir="output/detections", dest_dir="datasets/training"):
    """
    Organize images and labels into YOLO-compatible folder structure.
    """
    train_img_dir = os.path.join(dest_dir, "images/train")
    val_img_dir = os.path.join(dest_dir, "images/val")
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)

    images = [f for f in os.listdir(src_dir) if f.endswith(".png")]
    split_idx = int(len(images) * 0.8)
    train, val = images[:split_idx], images[split_idx:]

    for img in train:
        shutil.copy(os.path.join(src_dir, img), os.path.join(train_img_dir, img))
    for img in val:
        shutil.copy(os.path.join(src_dir, img), os.path.join(val_img_dir, img))

    logger.info(f"Dataset prepared: {len(train)} train | {len(val)} val images")
