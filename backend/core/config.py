import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PAGES_DIR = os.path.join(OUTPUT_DIR, "pages")
CROPS_DIR = os.path.join(OUTPUT_DIR, "crops")
OCR_DIR = os.path.join(OUTPUT_DIR, "ocr")
STRUCTURED_DIR = os.path.join(OUTPUT_DIR, "structured")

MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8_tile.pt")

# Create directories if missing
for d in [OUTPUT_DIR, PAGES_DIR, CROPS_DIR, OCR_DIR, STRUCTURED_DIR]:
    os.makedirs(d, exist_ok=True)

# Application constants
PDF_DPI = 300
MIN_CONFIDENCE = 0.6
