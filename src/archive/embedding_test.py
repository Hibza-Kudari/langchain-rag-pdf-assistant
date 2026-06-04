from sentence_transformers import SentenceTransformer

print("Starting...")

try:
    print("Loading model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Model loaded!")

    embedding = model.encode(
        "Morphological Image Processing"
    )

    print("Embedding length:", len(embedding))
    print(embedding[:10])

except Exception as e:
    print("ERROR:", e)