from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    dimensions: Optional[str]
    text: Optional[str]
    image_path: Optional[str]
    confidence: Optional[float]
