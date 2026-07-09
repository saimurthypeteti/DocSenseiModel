"""Question-answering service."""

import time

from chains.rag_chain import GroundedGenerationChain
from config import get_settings
from database.chroma_store import ChromaDocumentStore
from models.schemas import AnswerResult


class QAService:
    """Retrieve chunks and generate grounded answers."""

    def __init__(self) -> None:
        settings = get_settings()
        self.top_k = settings.top_k
        self.store = ChromaDocumentStore(settings.chroma_persist_dir)

    def answer(self, question: str) -> AnswerResult:
        """Answer a user question."""
        started = time.perf_counter()
        chunks = self.store.similarity_search(question, self.top_k)
        chain = GroundedGenerationChain()
        answer = chain.answer(question, chunks)
        citations = chain.citations_for(chunks) if chunks else []
        return AnswerResult(
            answer=answer,
            citations=citations,
            retrieved_chunks=chunks,
            response_time_seconds=time.perf_counter() - started,
        )
