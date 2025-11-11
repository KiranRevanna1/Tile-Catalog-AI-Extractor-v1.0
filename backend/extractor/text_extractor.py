def clean_ocr_text(text: str) -> str:
    """
    Basic cleaning: remove extra spaces, broken line breaks, and artifacts.
    """
    return " ".join(text.replace("\n", " ").split())
