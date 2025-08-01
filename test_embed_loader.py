from embed_loader import load_embedder

def test_embedding():
    embedder = load_embedder("nomic-embed-text")
    vec = embedder.get_text_embedding("Test this please")
    print("✅ Vector created! Length:", len(vec))
    print("🔢 Sample:", vec[:5])

if __name__ == "__main__":
    test_embedding()

