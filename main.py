# === main.py ===
# Entry point for the IT Helpdesk Assistant
# Supports --text and --image query modes via CLI
# Selects model via CLI argument (e.g., phi3 or mistral)

import sys
import os

# Import modules from other files
from llm_loader import load_llm
from embed_loader import load_embedder
from index_manager import get_or_build_index as get_index
from query_engine import get_query_engine
from ocr_utils import extract_text_from_image

# === Configuration ===
KB_PATH = "data"                   # Folder containing your KB (PDFs, text, screenshots)
INDEX_PATH = "index"              # Path to store/reuse vector index
EMBED_MODEL = "nomic-embed-text"  # Embedding model to be used for indexing/querying

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [model_name] --text 'question' OR --image path/to/screenshot.png")
        sys.exit(1)

    # Parse model name from CLI
    model_name = sys.argv[1]
    query = None

    # Handle --text or --image input
    if "--text" in sys.argv:
        query = sys.argv[sys.argv.index("--text") + 1]

    elif "--image" in sys.argv:
        image_path = sys.argv[sys.argv.index("--image") + 1]
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file '{image_path}' not found.")
            sys.exit(1)
        # Extract query text using OCR
        query = extract_text_from_image(image_path)
        print(f"[OCR EXTRACTED TEXT] → {query}")

    else:
        print("❌ Error: Please provide either --text or --image input.")
        sys.exit(1)

    # Load LLM (phi3, mistral, etc.)
    print(f"[INFO] Loading LLM: {model_name}")
    llm = load_llm(model_name)

    # Load embedding model (fixed: nomic-embed-text)
    print(f"[INFO] Loading embedding model: {EMBED_MODEL}")
    embedder = load_embedder(EMBED_MODEL)

    # Load or build the vector 
    
    print(f"[INFO] Loading or building vector index at: {INDEX_PATH}")
    index = get_index(embedder, KB_PATH, INDEX_PATH)


    # Build query engine (RAG pipeline)
    query_engine = get_query_engine(index, llm)

    # Run the query
    print("🤖 Querying knowledge base...")
    response = query_engine.query(query)

    print(f"\n🧠 Answer: {response.response}\n")

if __name__ == "__main__":
    main()

