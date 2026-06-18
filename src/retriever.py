import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
    RETRIEVAL_K,
)

_vectorstore = None
_embeddings = None


def vectorstore_exists():
    return os.path.exists(
        os.path.join(
            VECTORSTORE_DIR,
            "index.faiss",
        )
    )


def _get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    return _embeddings


def _load():
    global _vectorstore

    if _vectorstore is not None:
        return

    if not vectorstore_exists():
        raise FileNotFoundError(
            "No vector store found. Upload a PDF first."
        )

    _vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def reload():
    global _vectorstore

    _vectorstore = None
    _load()


def get_all_chunks():
    _load()

    docs = _vectorstore.similarity_search(
        "",
        k=100,
    )

    return [
        doc.page_content
        for doc in docs
    ]


def retrieve(
    query,
    k=RETRIEVAL_K,
):
    _load()

    docs = _vectorstore.similarity_search(
        query,
        k=k,
    )

    return [
        doc.page_content
        for doc in docs
    ]