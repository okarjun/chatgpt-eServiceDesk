# === index_manager.py ===
# Purpose: Incrementally update your vector index by adding only new or changed PDFs from /data

import os
import hashlib
import json
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Document
)
from ocr_utils import extract_all_pdfs_from_folder

HASH_STORE = "index/file_hashes.json"

def compute_file_hash(path):
    """Return MD5 hash of a file for change detection"""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_previous_hashes():
    if os.path.exists(HASH_STORE):
        with open(HASH_STORE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hash_dict):
    os.makedirs(os.path.dirname(HASH_STORE), exist_ok=True)
    with open(HASH_STORE, "w") as f:
        json.dump(hash_dict, f, indent=2)

def get_or_build_index(embed_model, data_path="data", index_path="index"):
    """
    Incrementally build or update a vector index from PDFs in /data.
    Only adds new or changed files using content hash comparison.
    """
    print("📁 Scanning /data for new or updated PDFs...")

    # Compute current hashes
    current_hashes = {}
    file_paths = []

    for root, _, files in os.walk(data_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                file_paths.append(full_path)
                current_hashes[full_path] = compute_file_hash(full_path)

    # Load previously indexed hashes
    previous_hashes = load_previous_hashes()

    # Identify new or modified files
    changed_files = [f for f in file_paths if current_hashes.get(f) != previous_hashes.get(f)]

    if not os.path.exists(index_path):
        print("🛠️ No existing index found. Creating new index...")
        storage_context = StorageContext.from_defaults()
        index = None
    else:
        print("📦 Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=index_path)
        index = load_index_from_storage(storage_context, embed_model=embed_model)

    if changed_files:
        print(f"🆕 Found {len(changed_files)} new or changed file(s). Processing...")

        # Extract OCR from only changed files
        extracted = extract_all_pdfs_from_folder(data_path)
        new_docs = [
            Document(text=doc["content"], metadata={"file": doc["filename"]})
            for doc in extracted
            if doc["filename"] in changed_files and doc["content"].strip()
        ]

        if index:
            index.insert_documents(new_docs)
        else:
            index = VectorStoreIndex.from_documents(new_docs, embed_model=embed_model)

        # Persist index and updated hash state
        index.storage_context.persist(persist_dir=index_path)
        save_hashes(current_hashes)
        print(f"✅ Indexed and saved {len(new_docs)} documents to '{index_path}'.")

    else:
        if index:
            print("✅ No changes found. Using existing index.")
        else:
            raise RuntimeError("❌ No existing index found and no new data to index.")

    return index

