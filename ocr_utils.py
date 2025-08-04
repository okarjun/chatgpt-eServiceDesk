# ocr_utils.py

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_image(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise RuntimeError(f"❌ OCR extraction failed from image: {e}")

def extract_text_from_pdf_with_screenshots(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        full_text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # OCR on embedded images
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text = pytesseract.image_to_string(image)
                full_text += f"\n[OCR Page {page_num+1} Image {img_index+1}]\n{text.strip()}\n"

            # Extract visible text
            text_layer = page.get_text()
            if text_layer.strip():
                full_text += f"\n[Text Page {page_num+1}]\n{text_layer.strip()}\n"

        return full_text.strip()

    except Exception as e:
        raise RuntimeError(f"❌ Failed to extract text from PDF '{pdf_path}': {e}")

def extract_all_pdfs_from_folder(folder_path: str) -> list:
    all_texts = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                print(f"🔍 Processing {pdf_path}")
                text = extract_text_from_pdf_with_screenshots(pdf_path)
                all_texts.append({
                    "filename": pdf_path,
                    "content": text
                })

    return all_texts

