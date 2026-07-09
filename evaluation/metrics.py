"""Evaluation metrics for retrieval experiments."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalMetrics:
    """Retrieval quality and timing metrics."""

    retrieval_accuracy: float
    precision_at_k: float
    recall_at_k: float
    average_response_time: float


def precision_at_k(retrieved: list[str], expected: set[str], k: int) -> float:
    """Calculate precision@k for retrieved chunk IDs."""
    if k <= 0:
        return 0.0
    top = retrieved[:k]
    if not top:
        return 0.0
    return len(set(top) & expected) / len(top)


def recall_at_k(retrieved: list[str], expected: set[str], k: int) -> float:
    """Calculate recall@k for retrieved chunk IDs."""
    if not expected:
        return 0.0
    return len(set(retrieved[:k]) & expected) / len(expected)


def retrieval_accuracy(retrieved: list[str], expected: set[str], k: int) -> float:
    """Return 1 if any expected chunk appears in top-k, else 0."""
    return 1.0 if set(retrieved[:k]) & expected else 0.0
