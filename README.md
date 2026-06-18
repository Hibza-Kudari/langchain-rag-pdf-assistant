# 📚 LangChain-Powered RAG Conversational AI Assistant

An intelligent Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents, generate AI-powered summaries, and ask context-aware questions using semantic search and local LLM inference.

Built with **LangChain**, **FAISS**, **HuggingFace Embeddings**, **Ollama (Llama 3.2)**, and **Streamlit**.

---

## 🚀 Features

✅ Upload and process PDF documents

✅ Semantic document search using vector embeddings

✅ Context-aware question answering

✅ Conversational memory for follow-up questions

✅ AI-generated document summaries

✅ Source-backed responses

✅ Local LLM inference using Ollama

✅ Interactive Streamlit UI

---

## 🏗️ System Architecture

```text
                    ┌──────────────┐
                    │   PDF File   │
                    └──────┬───────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Text Extraction    │
                │ (PyPDF)            │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Text Chunking      │
                │ LangChain Splitter │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ MiniLM Embeddings  │
                │ HuggingFace        │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ FAISS Vector Store │
                │ (LangChain)        │
                └─────────┬──────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ LangChain       │
                 │ Retriever       │
                 └───────┬─────────┘
                         │
         User Query      ▼
      ─────────────► Relevant Chunks
                         │
                         ▼
                ┌────────────────────┐
                │ Ollama (Llama 3.2) │
                └─────────┬──────────┘
                          │
                          ▼
                   Final Response
```

---

## 🧠 How It Works

1. User uploads a PDF document.
2. PDF text is extracted and split into semantic chunks.
3. Chunks are converted into vector embeddings using MiniLM.
4. Embeddings are stored in a FAISS vector database.
5. User asks a question.
6. LangChain Retriever finds the most relevant chunks.
7. Retrieved context is sent to Ollama (Llama 3.2).
8. The model generates a source-grounded answer.

---

## 📊 Performance Observations

| Document Size | Chunks Generated |
| ------------- | ---------------- |
| 9 Pages       | 6 Chunks         |
| 14 Pages      | 23 Chunks        |
| 32 Pages      | 56 Chunks        |

Example query response times:

| Query      | Time         |
| ---------- | ------------ |
| Question 1 | 2 min 03 sec |
| Question 2 | 1 min 55 sec |
| Question 3 | 2 min 26 sec |

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* FAISS
* HuggingFace Embeddings
* Ollama
* Llama 3.2
* PyPDF

---

## 📂 Project Structure

```text
rag-chatbot/
│
├── src/
│   ├── app.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── config.py
│
├── vectorstore/
│
├── requirements.txt
│
└── README.md
```

---

## 📸 Screenshots


### PDF Upload

```text
assets/upload.png
```

### Question Answering


```text
assets/chat.png
```

### Document Summary

```text
assets/summary.png
```

---

## 🔮 Future Enhancements

* Multi-PDF Support
* Citation with Page Numbers
* ChromaDB / Pinecone Integration
* Advanced Memory Management
* Document Comparison
* Multi-Agent RAG Workflow

---

## 👩‍💻 Author

**Hibza Kudari**

AI & Machine Learning Student

Passionate about Generative AI, RAG Systems, LLM Applications, and Intelligent Document Processing.
