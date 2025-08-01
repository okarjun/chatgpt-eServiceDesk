# === ocr_utils.py ===
# Utility to extract text from a screenshot or image using OCR (Tesseract)

import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    """
    Extract readable text from an image using OCR.

    Args:
        image_path: Path to the screenshot or image file (e.g., PNG, JPG)

    Returns:
        Extracted text as a string
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found: {image_path}")
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print(f"🧾 OCR extracted text:\n{text[:300]}...")  # Show sample
        return text
    except Exception as e:
        raise RuntimeError(f"❌ OCR failed on '{image_path}': {e}")

