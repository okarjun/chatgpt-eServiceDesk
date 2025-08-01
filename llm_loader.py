# === llm_loader.py ===
# Loads local LLMs from Ollama by name (phi3, mistral, llama3, etc.)

from langchain_ollama import ChatOllama

def load_llm(model_name: str = "phi3"):
    """
    Load a local language model served by Ollama.

    Args:
        model_name: The name of the Ollama model to load (default = "phi3")

    Returns:
        A ChatOllama instance you can use for querying
    """
    try:
        return ChatOllama(model=model_name)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load LLM '{model_name}': {e}")

