from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

reader = PdfReader("documents/DIP_4.pdf")

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(full_text)

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(embeddings.shape[1])

index.add(np.array(embeddings).astype("float32"))

print("Chunks:", len(chunks))
print("Vectors:", index.ntotal)