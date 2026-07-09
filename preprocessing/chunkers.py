"""Chunking strategies for document pages."""

from enum import Enum

from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.schemas import DocumentChunk, LoadedPage


class ChunkStrategy(str, Enum):
    """Supported chunking strategies."""

    FIXED = "Fixed Chunking"
    RECURSIVE = "Recursive Character"


class DocumentChunker:
    """Create chunks using selectable strategies."""

    def __init__(self, chunk_size: int = 500, overlap: int = 100) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(
        self,
        pages: list[LoadedPage],
        strategy: ChunkStrategy,
    ) -> list[DocumentChunk]:
        """Chunk pages and attach deterministic chunk IDs."""
        chunks: list[DocumentChunk] = []
        for page in pages:
            parts = (
                self._fixed_chunks(page.text)
                if strategy == ChunkStrategy.FIXED
                else self._recursive_chunks(page.text)
            )
            for index, text in enumerate(parts, start=1):
                chunk_id = f"{page.document_name}:p{page.page_number}:c{index}"
                chunks.append(
                    DocumentChunk(
                        document_name=page.document_name,
                        page_number=page.page_number,
                        chunk_id=chunk_id,
                        text=text,
                        source=page.source,
                    )
                )
        return chunks

    def _fixed_chunks(self, text: str) -> list[str]:
        cleaned = text.strip()
        if not cleaned:
            return []
        step = max(self.chunk_size - self.overlap, 1)
        return [
            cleaned[start : start + self.chunk_size].strip()
            for start in range(0, len(cleaned), step)
            if cleaned[start : start + self.chunk_size].strip()
        ]

    def _recursive_chunks(self, text: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap,
        )
        return [part.strip() for part in splitter.split_text(text) if part.strip()]
