from io import BytesIO
from pathlib import Path
import os

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
)


def _read_pdf(source):
    if isinstance(source, (str, Path)):
        return PdfReader(source)

    if isinstance(source, bytes):
        return PdfReader(BytesIO(source))

    return PdfReader(source)


def ingest_pdf(source) -> int:
    """
    Build a LangChain FAISS vector store
    from a PDF path, bytes, or file-like object.
    """

    reader = _read_pdf(source)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text

    if not full_text.strip():
        raise ValueError(
            "Could not extract any text from the PDF."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(full_text)

    print(f"Total Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- CHUNK {i} ---")
        print(chunk[:300])  # first 300 chars

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings,
    )

    os.makedirs(
        VECTORSTORE_DIR,
        exist_ok=True,
    )

    vectorstore.save_local(
        VECTORSTORE_DIR
    )

    return len(chunks)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python ingest.py <path-to-pdf>"
        )
        sys.exit(1)

    count = ingest_pdf(sys.argv[1])

    print(
        f"Done! Ingested {count} chunks."
    )