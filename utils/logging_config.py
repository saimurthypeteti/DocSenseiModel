"""Logging configuration."""

import logging

from config import get_settings


def configure_logging() -> None:
    """Configure process-wide logging once."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
