==============================
🧠 How to Start the Helpdesk Chatbot
==============================

1. Activate the Python virtual environment:

   cd ~/chatgpt-eServiceDesk
   source rag-env/bin/activate

2. Ask a text-based question (example):

   python main.py phi3 --text "How do I reset my VPN password?"

3. Ask using a screenshot image (example):

   python main.py phi3 --image data/error.png

Note:
- Replace 'phi3' with any other installed model name like 'mistral'
- Ensure the image exists inside the 'data' folder before running

Optional:
You can add more knowledge base files to the 'data' folder anytime.
To rebuild the vector index, delete the 'index' folder and re-run the script.

