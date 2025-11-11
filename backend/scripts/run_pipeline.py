import argparse
from extractor.pdf_pipeline import process_pdf

def main():
    parser = argparse.ArgumentParser(description="Run Tile Catalog AI extraction pipeline.")
    parser.add_argument("--pdf", required=True, help="Path to input PDF file")
    args = parser.parse_args()

    result = process_pdf(args.pdf)
    print("\n✅ Extraction completed successfully!")
    print(f"Processed {len(result['pages'])} pages and extracted {len(result['ocr'])} OCR items.\n")

if __name__ == "__main__":
    main()
