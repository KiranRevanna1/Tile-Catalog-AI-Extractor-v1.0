import fitz  # PyMuPDF
import os
from core.logger import get_logger
from core.config import PDF_DPI

logger = get_logger(__name__)

def pdf_to_images(pdf_path, output_dir="output/pages", dpi=PDF_DPI):
    """
    Converts PDF pages to high-resolution images and saves them to disk.
    Returns a list of saved image paths.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page_images = []

    logger.info(f"Converting {len(doc)} pages from PDF → {output_dir}")

    for page_num, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=dpi)
        img_path = os.path.join(output_dir, f"page_{page_num}.png")
        pix.save(img_path)
        page_images.append(img_path)
        logger.info(f"Page {page_num} saved → {img_path}")

    doc.close()
    return page_images
