from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os, shutil
from extractor.pdf_pipeline import process_pdf
from extractor.formatter import structure_products
from routes.feedback import router as feedback_router

app = FastAPI(title="Tile Catalog AI Extractor API")

# Include other routers
app.include_router(feedback_router)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract")
async def extract_data(file: UploadFile = File(...)):
    upload_dir = "uploads"
    output_dir = "output"

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Save uploaded file
    pdf_path = os.path.join(upload_dir, file.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 1–3: YOLO + OCR pipeline
    extracted_data = process_pdf(pdf_path, output_dir)

    # Step 4: Structure data into products
    structured = structure_products(extracted_data, output_dir)

    return {"products": structured, "count": len(structured)}
