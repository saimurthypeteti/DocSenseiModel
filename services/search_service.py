"""Semantic search service."""

from config import get_settings
from database.chroma_store import ChromaDocumentStore
from models.schemas import DocumentChunk


class SearchService:
    """Run semantic search over indexed documents."""

    def __init__(self) -> None:
        settings = get_settings()
        self.store = ChromaDocumentStore(settings.chroma_persist_dir)
        self.top_k = settings.top_k

    def search(self, query: str) -> list[DocumentChunk]:
        """Return semantically similar chunks."""
        return self.store.similarity_search(query, self.top_k)
