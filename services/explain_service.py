"""Explanation service."""

from chains.rag_chain import GroundedGenerationChain
from config import get_settings
from database.chroma_store import ChromaDocumentStore


class ExplainService:
    """Explain selected sections at different levels."""

    def __init__(self) -> None:
        settings = get_settings()
        self.store = ChromaDocumentStore(settings.chroma_persist_dir)
        self.top_k = settings.top_k

    def explain(self, section_query: str, level: str) -> str:
        """Explain the most relevant sections for a query."""
        chunks = self.store.similarity_search(section_query, self.top_k)
        return GroundedGenerationChain().explain(level, chunks)
