"""Custom exceptions for predictable UI error handling."""


class DocSenseiError(Exception):
    """Base application error."""


class InvalidFileError(DocSenseiError):
    """Raised when an uploaded file type is unsupported."""


class EmptyDocumentError(DocSenseiError):
    """Raised when no readable text is extracted."""


class VectorStoreError(DocSenseiError):
    """Raised when the vector database is unavailable."""


class MissingApiKeyError(DocSenseiError):
    """Raised when an LLM call is requested without an API key."""
