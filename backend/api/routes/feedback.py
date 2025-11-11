from fastapi import APIRouter
from pydantic import BaseModel
import shutil, os, uuid

router = APIRouter()

DATASET_DIR = "backend/training/datasets"
os.makedirs(f"{DATASET_DIR}/images", exist_ok=True)
os.makedirs(f"{DATASET_DIR}/labels", exist_ok=True)

class Feedback(BaseModel):
    image: str
    correct: bool

@router.post("/feedback")
def save_feedback(data: Feedback):
    image_path = data.image
    if not os.path.exists(image_path):
        return {"status": "error", "message": "Image not found"}

    img_id = uuid.uuid4().hex
    dest_path = os.path.join(DATASET_DIR, "images", f"{img_id}.jpg")

    shutil.copy(image_path, dest_path)

    # Save label file (1 = correct, 0 = incorrect)
    label_path = os.path.join(DATASET_DIR, "labels", f"{img_id}.txt")
    with open(label_path, "w") as f:
        f.write("1" if data.correct else "0")

    return {"status": "ok", "saved": dest_path}
