"""Summary service."""

from chains.rag_chain import GroundedGenerationChain
from config import get_settings
from database.chroma_store import ChromaDocumentStore


class SummaryService:
    """Generate grounded summaries."""

    def __init__(self) -> None:
        settings = get_settings()
        self.store = ChromaDocumentStore(settings.chroma_persist_dir)
        self.top_k = max(settings.top_k, 8)

    def summarize(self, query: str, summary_type: str) -> str:
        """Summarize chunks relevant to a summary query."""
        chunks = self.store.similarity_search(query, self.top_k)
        return GroundedGenerationChain().summarize(summary_type, chunks)
