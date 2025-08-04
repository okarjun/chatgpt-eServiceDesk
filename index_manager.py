# === index_manager.py ===
# Purpose: Load a saved vector index OR build a new one from local knowledge base files,
#          including text extracted from PDFs with screenshots using OCR.

import os
from llama_index.core import (
    VectorStoreIndex,         # Core index that supports vector search
    StorageContext,           # Manages saving/loading index state
    load_index_from_storage,  # Loads a previously saved index
    Document                  # Schema for raw document content
)

from ocr_utils import extract_all_pdfs_from_folder  # OCR function for scanned/screenshot PDFs

def get_or_build_index(embed_model, data_path="data", index_path="index"):
    """
    Load or build a vector index from the /data folder.

    This version supports OCR for screenshots embedded in PDFs using PyMuPDF and Tesseract.

    Args:
        embed_model: The embedding model used to convert text into vector format.
        data_path (str): Path to folder containing knowledge base documents (PDF, DOCX, etc.).
        index_path (str): Path to folder where the vector index will be stored.

    Returns:
        VectorStoreIndex: A searchable index for your RAG-based assistant.

    How it works:
    - If the index already exists, it loads from disk (fast startup).
    - Otherwise, it:
      1. Extracts content from ALL PDFs in /data (including OCR of screenshots),
      2. Wraps them as `Document` objects,
      3. Builds a fresh vector index,
      4. Saves it to /index.
    """

    if os.path.exists(index_path):
        print(f"📦 Loading existing index from '{index_path}'...")
        storage_context = StorageContext.from_defaults(persist_dir=index_path)
        return load_index_from_storage(storage_context, embed_model=embed_model)

    print(f"📄 No index found. Extracting documents from '{data_path}'...")
    extracted = extract_all_pdfs_from_folder(data_path)

    if not extracted:
        raise RuntimeError(f"❌ No valid PDFs found in '{data_path}'.")

    documents = [
        Document(text=entry["content"], metadata={"file": entry["filename"]})
        for entry in extracted if entry["content"].strip()
    ]

    print(f"✅ Extracted and processed {len(documents)} PDFs.")

    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=index_path)
    print(f"💾 New index created and saved to '{index_path}'.")

    return index

