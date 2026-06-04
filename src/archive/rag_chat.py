from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama

# Read PDF
reader = PdfReader("documents/DIP_4.pdf")

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text

# Chunking
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(full_text)

# Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

# Vector DB
index = faiss.IndexFlatL2(embeddings.shape[1])

index.add(np.array(embeddings).astype("float32"))

# Question
query = input("Ask a question: ")

query_embedding = model.encode([query])

distances, indices = index.search(
    np.array(query_embedding).astype("float32"),
    k=3
)

context = "\n\n".join(
    [chunks[i] for i in indices[0]]
)

prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAnswer:\n")
print(response["message"]["content"])