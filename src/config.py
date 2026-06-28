import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
CHUNKS_PATH = os.path.join(VECTORSTORE_DIR, "chunks.pkl")
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, "faiss_index.bin")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"    
RETRIEVAL_K = 4
