from embed_loader import load_embedder
from index_manager import get_or_build_index

def test_index():
    embed_model = load_embedder("nomic-embed-text")
    index = get_or_build_index(embed_model, data_path="data", index_path="index")
    print("✅ Index is ready.")
    print(f"🔎 Index summary: {index}")

if __name__ == "__main__":
    test_index()

