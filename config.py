"""Application configuration for DocSensei."""


from functools import lru_cache
from pathlib import Path
import tempfile

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "DocSensei"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""
    llm_base_url: str | None = None
    llm_temperature: float = 0.0
    chroma_persist_dir: Path = Path(tempfile.gettempdir()) / "vectorstore"
    upload_dir: Path = Path(tempfile.gettempdir()) / "uploads"
    top_k: int = Field(default=4, ge=1, le=20)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def ensure_directories(self) -> None:
        """Create local runtime directories if missing."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    settings = Settings()
    settings.ensure_directories()
    return settings
