"""Helpers for validating and saving uploaded files."""

from pathlib import Path
from uuid import uuid4

from models.schemas import SavedFile
from utils.errors import InvalidFileError

ALLOWED_SUFFIXES = {".pdf", ".docx"}


class UploadManager:
    """Persist Streamlit uploads to disk."""

    def __init__(self, upload_dir: Path) -> None:
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_files(self, uploaded_files: list) -> list[SavedFile]:
        """Validate and save uploaded files."""
        saved: list[SavedFile] = []
        for file in uploaded_files:
            original_name = Path(file.name).name
            suffix = Path(original_name).suffix.lower()
            if suffix not in ALLOWED_SUFFIXES:
                raise InvalidFileError(f"Unsupported file type: {original_name}")
            safe_name = f"{Path(original_name).stem}_{uuid4().hex[:8]}{suffix}"
            path = self.upload_dir / safe_name
            path.write_bytes(file.getbuffer())
            saved.append(SavedFile(original_name=original_name, path=path, suffix=suffix))
        return saved
