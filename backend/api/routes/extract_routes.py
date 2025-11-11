from fastapi import APIRouter, UploadFile, File
from api.services.extraction_service import process_uploaded_pdf

router = APIRouter()

@router.post("/")
async def extract_data(file: UploadFile = File(...)):
    contents = await file.read()
    result = process_uploaded_pdf(contents, file.filename)
    return result
