import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path, output_dir="output/pages", dpi=300):
    """
    Converts each page in a PDF into a high-resolution image.
    Returns a list of image file paths.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"[ERROR] PDF not found: {pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    print(f"[INFO] Converting PDF to images → {output_dir}")

    doc = fitz.open(pdf_path)
    page_images = []

    for page_num, page in enumerate(doc):
        try:
            pix = page.get_pixmap(dpi=dpi)
            img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
            pix.save(img_path)
            page_images.append(img_path)
            print(f"  [OK] Saved page {page_num + 1}/{len(doc)} → {img_path}")
        except Exception as e:
            print(f"  [ERROR] Failed on page {page_num + 1}: {e}")

    doc.close()

    if not page_images:
        raise RuntimeError("[ERROR] No images were generated from the PDF.")

    print(f"[SUCCESS] Extracted {len(page_images)} page images.\n")
    return page_images
