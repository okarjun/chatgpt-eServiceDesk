# === index_manager.py ===
# Purpose: Load a saved vector index OR build a new one from local knowledge base files

import os
from llama_index.core import (
    SimpleDirectoryReader,   # Reads PDF/TXT/DOCX/etc. from the /data folder
    VectorStoreIndex,        # Core index that supports vector search
    StorageContext,          # Manages saving/loading index state
    load_index_from_storage  # Loads a previously saved index
)

def get_or_build_index(embed_model, data_path="data", index_path="index"):
    """
    Load or build a vector index from knowledge base files.

    Args:
        embed_model: Embedding model to convert documents to vectors
        data_path: Folder where your source files (PDFs, text) are stored
        index_path: Folder where the processed vector index will be saved

    Returns:
        An initialized VectorStoreIndex object that can be used in query engine

    How it works:
    - If /index exists → load the vector index directly (faster startup)
    - Else → scan all files in /data, embed them, create index, and save it to /index
    """

    if os.path.exists(index_path):
        print(f"📦 Loading existing index from '{index_path}'...")
        storage_context = StorageContext.from_defaults(persist_dir=index_path)
        index = load_index_from_storage(storage_context, embed_model=embed_model)
    else:
        print(f"📄 No index found. Building new index from '{data_path}'...")
        documents = SimpleDirectoryReader(data_path).load_data()
        print(f"✅ Loaded {len(documents)} documents.")

        # Create a new vector index from document embeddings
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

        # Save to disk for future reuse
        index.storage_context.persist(persist_dir=index_path)
        print(f"💾 Index saved to '{index_path}'")

    return index

