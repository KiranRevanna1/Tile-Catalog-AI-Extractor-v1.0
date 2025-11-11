from pydantic import BaseModel
from typing import List, Optional

class PDFExtractRequest(BaseModel):
    filename: str
    file_bytes: bytes

class PDFExtractResponse(BaseModel):
    filename: str
    products: List[dict]
