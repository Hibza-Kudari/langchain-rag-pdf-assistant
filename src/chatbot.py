from retriever import retrieve
import ollama

while True:

    query = input("\nAsk a question (or type exit): ")

    if query.lower() == "exit":
        break

    chunks = retrieve(query)

    context = "\n\n".join(chunks)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

If the answer is not in the context, say:
"I could not find that information in the document."
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
    print(
        response["message"]["content"]
    )