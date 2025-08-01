# === query_engine.py ===
# Responsible for connecting the index with the LLM to answer user queries

from llama_index.core.query_engine import RetrieverQueryEngine

def get_query_engine(index, llm):
    """
    Set up and return a query engine using the provided index and LLM.
    """
    return index.as_query_engine(llm=llm)

