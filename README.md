# 🤖 ChatGPT-powered IT Helpdesk Assistant (Local RAG + OCR)

A modular AI chatbot built using local language models (like Phi-3 or Mistral) that reads your internal knowledge base (PDFs, text, screenshots) and answers IT support questions with high accuracy.

---

## 📦 What This Project Can Do

- ✅ Answer user queries based on your IT Helpdesk knowledge base (KB)
- ✅ Extract text from screenshots (e.g. error messages) using OCR
- ✅ Run locally with no internet — all models served via Ollama
- ✅ Easy to switch models (like Phi3, Mistral, LLaMA3)
- ✅ Fully modular — replace any component (LLM, embedder, OCR, etc.)

---

## 📁 Folder Structure

chatgpt-eServiceDesk/
├── data/           # Place your PDF, DOCX, or TXT KB articles here
├── index/          # Auto-generated vector index for faster querying
├── rag-env/        # Python virtual environment
├── main.py         # CLI chatbot interface
├── llm_loader.py   # Loads language model from Ollama
├── embed_loader.py # Loads embedding model (for document search)
├── index_manager.py# Loads or builds vector index
├── query_engine.py # Combines LLM + index for answering
├── ocr_utils.py    # Extracts text from screenshots using OCR
├── requirements.txt# Python dependencies

---

## 🚀 How to Run It

### 1. Clone and Setup Environment

cd /home/chatgpt
git clone <this-repo> chatgpt-eServiceDesk
cd chatgpt-eServiceDesk
python3 -m venv rag-env
source rag-env/bin/activate

### 2. Install Dependencies

pip install -r requirements.txt

Also install OCR system tool:

sudo dnf install tesseract tesseract-langpack-eng

### 3. Install a Local Model (e.g. Phi3)

ollama pull phi3

### 4. Add Knowledge Base Docs

Put your PDF or text files into the `/data/` folder

---

## 💬 How to Use It

### Ask a text question

python main.py phi3 --text "How to unlock a suspended AD account?"

### Ask a screenshot question

python main.py mistral --image data/error_screenshot.png

---

## 🔄 Switch Models Easily

You can switch to another LLM by pulling it from Ollama:

ollama pull mistral

Then use it:

python main.py mistral --text "What's the VPN timeout error code?"

---

## 🧠 Why This Project?

- Many IT teams have PDFs or articles but no smart chatbot.
- This assistant bridges that gap — powered by local models + your real documents.
- Runs 100% offline on your HP EliteBook (i7 13th gen, 16GB RAM).

---

## 🛠️ Credits & Tech Stack

- Langchain
- LlamaIndex
- Ollama
- Tesseract OCR

---

## ✅ To Do Next

- [ ] Add Chat UI (Streamlit or Gradio)
- [ ] Add CSV/Excel support
- [ ] Add basic logging and feedback rating
- [ ] Deploy via Docker for easy reuse

---

> Built with ❤️ on Oracle Linux 9 for HP EliteBook

