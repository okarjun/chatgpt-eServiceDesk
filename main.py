# === main.py ===
# Entry point for querying the local RAG assistant with --text, --image, or --pdf

import sys
import os

from llm_loader import load_llm
from embed_loader import load_embedder
from index_manager import get_or_build_index
from query_engine import get_query_engine

from ocr_utils import extract_text_from_image, extract_text_from_pdf_with_screenshots

# Configuration
KB_PATH = "data"
INDEX_PATH = "index"
EMBED_MODEL = "nomic-embed-text"

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [model_name] --text 'query' OR --image file OR --pdf file")
        sys.exit(1)

    model_name = sys.argv[1]
    query = None

    if "--text" in sys.argv:
        query = sys.argv[sys.argv.index("--text") + 1]

    elif "--image" in sys.argv:
        image_path = sys.argv[sys.argv.index("--image") + 1]
        if not os.path.exists(image_path):
            print(f"❌ Image file '{image_path}' not found.")
            sys.exit(1)
        query = extract_text_from_image(image_path)
        print(f"[OCR EXTRACTED TEXT FROM IMAGE] → {query}")

    elif "--pdf" in sys.argv:
        pdf_path = sys.argv[sys.argv.index("--pdf") + 1]
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file '{pdf_path}' not found.")
            sys.exit(1)
        query = extract_text_from_pdf_with_screenshots(pdf_path)
        print(f"[OCR EXTRACTED TEXT FROM PDF] → {query[:500]}...")

    else:
        print("❌ Please provide --text, --image, or --pdf input.")
        sys.exit(1)

    # Load LLM and embedder
    llm = load_llm(model_name)
    embedder = load_embedder(EMBED_MODEL)

    # Load or build index
    index = get_or_build_index(embedder, KB_PATH, INDEX_PATH)
    query_engine = get_query_engine(index, llm)

    print("🤖 Querying KB...")
    response = query_engine.query(query)

    # 🧠 Print the final answer
    print(f"\n🧠 Answer: {response.response}\n")

    # 📚 Show source documents used
    if hasattr(response, "source_nodes") and response.source_nodes:
        print("📚 Sources used:")
        for i, source_node in enumerate(response.source_nodes, 1):
            source = source_node.node.metadata.get("file", "Unknown")
            snippet = source_node.node.text.strip()[:200].replace("\n", " ")
            print(f"  {i}. {source} → \"{snippet}...\"")

if __name__ == "__main__":
    main()

