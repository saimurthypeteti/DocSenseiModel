"""Document indexing service."""

from config import get_settings
from database.chroma_store import ChromaDocumentStore
from loaders.document_loader import DocumentLoader
from loaders.file_manager import UploadManager
from preprocessing.chunkers import ChunkStrategy, DocumentChunker


class DocumentService:
    """Coordinate upload, extraction, chunking, and indexing."""

    def __init__(self) -> None:
        settings = get_settings()
        self.uploads = UploadManager(settings.upload_dir)
        self.loader = DocumentLoader()
        self.chunker = DocumentChunker()
        self.store = ChromaDocumentStore(settings.chroma_persist_dir)

    def index_uploads(self, uploaded_files: list, strategy: ChunkStrategy) -> int:
        """Save and index uploaded files, returning chunk count."""
        saved_files = self.uploads.save_files(uploaded_files)
        all_chunks = []
        for saved_file in saved_files:
            pages = self.loader.load(saved_file)
            all_chunks.extend(self.chunker.chunk_pages(pages, strategy))
        self.store.add_chunks(all_chunks)
        return len(all_chunks)

    def clear_database(self) -> None:
        """Clear Chroma database."""
        self.store.clear()

    def indexed_count(self) -> int:
        """Return current vector count."""
        return self.store.count()
