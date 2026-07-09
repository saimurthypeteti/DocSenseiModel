"""Typed schemas used across DocSensei."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class LoadedPage:
    """Extracted page-level document content."""

    document_name: str
    page_number: int
    text: str
    source: str


@dataclass(frozen=True)
class DocumentChunk:
    """Chunk prepared for embedding and retrieval."""

    document_name: str
    page_number: int
    chunk_id: str
    text: str
    source: str

    @property
    def metadata(self) -> dict[str, str | int]:
        """Return metadata persisted with the vector database record."""
        return {
            "document_name": self.document_name,
            "page_number": self.page_number,
            "chunk_id": self.chunk_id,
            "source": self.source,
        }


@dataclass(frozen=True)
class Citation:
    """Source citation displayed with answers."""

    document_name: str
    page_number: int
    chunk_id: str


@dataclass
class AnswerResult:
    """RAG answer with citations and retrieved context."""

    answer: str
    citations: list[Citation] = field(default_factory=list)
    retrieved_chunks: list[DocumentChunk] = field(default_factory=list)
    response_time_seconds: float = 0.0


@dataclass(frozen=True)
class SavedFile:
    """Saved uploaded file metadata."""

    original_name: str
    path: Path
    suffix: str
