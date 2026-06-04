from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

print("Reading PDF...")

reader = PdfReader("documents/uploaded.pdf")

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text

print("Chunking document...")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=100
)

chunks = splitter.split_text(full_text)

print("Number of chunks:", len(chunks))

print("Creating embeddings...")

try:
    print("Loading model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Model loaded!")

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    print("Embeddings created!")

except Exception as e:
    print("ERROR:", e)
    raise

print("Embeddings shape:", embeddings.shape)

print("Building FAISS index...")

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(
    np.array(embeddings).astype("float32")
)

print("Saving vector database...")

faiss.write_index(
    index,
    "vectorstore/faiss_index.bin"
)

with open(
    "vectorstore/chunks.pkl",
    "wb"
) as f:
    pickle.dump(chunks, f)

print("Done!")
print("Chunks:", len(chunks))