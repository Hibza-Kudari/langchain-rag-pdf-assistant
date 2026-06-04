# PDF RAG Chatbot

AI-powered PDF chatbot using Streamlit, Ollama, FAISS and Sentence Transformers.

## Features

* Upload and chat with any PDF document
* Semantic search using vector embeddings
* Retrieval-Augmented Generation (RAG)
* Local LLM inference using Ollama
* Streamlit web interface
* Chat history support
* Source citations for answers
* PDF summarization

## Tech Stack

* Python
* Streamlit
* FAISS
* Sentence Transformers
* Ollama
* Llama 3.2

## Project Structure

```text
rag-chatbot/
├── documents/
│   └── README.txt
├── src/
│   ├── app.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── chatbot.py
│   └── archive/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/Hibza-Kudari/rag-chatbot.git
cd rag-chatbot
```

2. Create a virtual environment

```bash
python -m venv venv312
```

3. Activate the environment

```bash
venv312\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Install Ollama and pull a model

```bash
ollama pull llama3.2
```

## Run the Application

```bash
streamlit run src/app.py
```

## Usage

1. Launch the Streamlit application.
2. Upload any PDF document.
3. Build the knowledge base.
4. Ask questions about the uploaded document.
5. View source chunks used to generate answers.

## Future Improvements

* Faster retrieval
* Multi-PDF support
* Conversation memory
* Document comparison
* Cloud deployment

## Author

Hibza Kudari
