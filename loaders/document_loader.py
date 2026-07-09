"""PDF and DOCX text extraction."""

import logging
from pathlib import Path

import docx2txt
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from models.schemas import LoadedPage, SavedFile
from utils.errors import EmptyDocumentError, InvalidFileError

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Load supported document formats into page-like records."""

    def load(self, saved_file: SavedFile) -> list[LoadedPage]:
        """Load a saved file into page records."""
        if saved_file.suffix == ".pdf":
            return self._load_pdf(saved_file.path, saved_file.original_name)
        if saved_file.suffix == ".docx":
            return self._load_docx(saved_file.path, saved_file.original_name)
        raise InvalidFileError(f"Unsupported file type: {saved_file.original_name}")

    def _load_pdf(self, path: Path, document_name: str) -> list[LoadedPage]:
        try:
            reader = PdfReader(str(path))
        except PdfReadError as exc:
            raise InvalidFileError(f"Corrupted or unreadable PDF: {document_name}") from exc

        pages: list[LoadedPage] = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(
                    LoadedPage(
                        document_name=document_name,
                        page_number=index,
                        text=text,
                        source=str(path),
                    )
                )
        if not pages:
            raise EmptyDocumentError(f"No readable text found in {document_name}")
        return pages

    def _load_docx(self, path: Path, document_name: str) -> list[LoadedPage]:
        text = docx2txt.process(str(path)) or ""
        if not text.strip():
            raise EmptyDocumentError(f"No readable text found in {document_name}")
        # DOCX does not expose stable page numbers without rendering, so use page 1.
        return [
            LoadedPage(
                document_name=document_name,
                page_number=1,
                text=text,
                source=str(path),
            )
        ]
