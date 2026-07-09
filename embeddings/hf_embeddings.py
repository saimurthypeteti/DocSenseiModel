"""HuggingFace embedding factory."""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from config import get_settings


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    """Return cached embedding model."""
    settings = get_settings()
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
