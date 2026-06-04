from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

chunks = [
    "Morphological image processing uses structuring elements.",
    "Histogram equalization improves image contrast.",
    "Edge detection identifies object boundaries."
]

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype("float32"))

query = "What is morphology in image processing?"

query_embedding = model.encode([query])

distances, indices = index.search(
    np.array(query_embedding).astype("float32"),
    k=1
)

print("Best match:")
print(chunks[indices[0][0]])