from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

# Load vector database
index = faiss.read_index(
    "vectorstore/faiss_index.bin"
)

# Load chunks
with open(
    "vectorstore/chunks.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve(query, k=2):

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(query_embedding).astype(
            "float32"
        ),
        k
    )

    results = []

    for i in indices[0]:
        results.append(
            chunks[i]
        )

    return results


if __name__ == "__main__":

    question = input(
        "Ask a question: "
    )

    results = retrieve(
        question
    )

    print("\nResults:\n")

    for chunk in results:
        print(chunk)
        print(
            "\n" + "=" * 50 + "\n"
        )