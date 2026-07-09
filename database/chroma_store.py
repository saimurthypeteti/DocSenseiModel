"""Chroma vector store integration."""

import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from embeddings.hf_embeddings import get_embeddings
from models.schemas import DocumentChunk
from utils.errors import VectorStoreError


class ChromaDocumentStore:
    """Persist and query document chunks in ChromaDB."""

    def __init__(self, persist_dir: Path, collection_name: str = "docsensei") -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.persist_dir.mkdir(parents=True, exist_ok=True)

    def _store(self) -> Chroma:
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=get_embeddings(),
            persist_directory=str(self.persist_dir),
        )

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Embed and save chunks."""
        if not chunks:
            raise VectorStoreError("No chunks were generated for indexing.")
        docs = [
            Document(page_content=chunk.text, metadata=chunk.metadata)
            for chunk in chunks
        ]
        ids = [chunk.chunk_id for chunk in chunks]
        self._store().add_documents(docs, ids=ids)

    def similarity_search(self, query: str, top_k: int) -> list[DocumentChunk]:
        """Retrieve top-k similar chunks."""
        docs = self._store().similarity_search(query, k=top_k)
        return [self._to_chunk(doc) for doc in docs]

    def count(self) -> int:
        """Return indexed vector count."""
        try:
            return int(self._store()._collection.count())
        except Exception as exc:
            raise VectorStoreError("Vector database is not available.") from exc

    def clear(self) -> None:
        """Delete the persisted vector database."""
        if self.persist_dir.exists():
            shutil.rmtree(self.persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _to_chunk(document: Document) -> DocumentChunk:
        metadata = document.metadata
        return DocumentChunk(
            document_name=str(metadata.get("document_name", "Unknown")),
            page_number=int(metadata.get("page_number", 1)),
            chunk_id=str(metadata.get("chunk_id", "")),
            text=document.page_content,
            source=str(metadata.get("source", "")),
        )
