# === embed_loader.py ===
# Loads the embedding model used to convert documents into vectors

from llama_index.embeddings.ollama import OllamaEmbedding

def load_embedder(model_name: str):
    """
    Load an embedding model via Ollama (default: 'nomic-embed-text').
    Used during both indexing and querying in RAG.
    """
    try:
        return OllamaEmbedding(model_name=model_name)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load embedding model '{model_name}': {e}")

