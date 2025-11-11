import shutil
import os
from core.config import OUTPUT_DIR

def clean_output():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)
        print("🧹 Output directory cleaned successfully.")

if __name__ == "__main__":
    clean_output()
