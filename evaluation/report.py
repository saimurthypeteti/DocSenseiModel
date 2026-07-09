"""Generate evaluation reports comparing chunking strategies."""

import time
from pathlib import Path

from evaluation.metrics import (
    RetrievalMetrics,
    precision_at_k,
    recall_at_k,
    retrieval_accuracy,
)


def evaluate_queries(
    strategy_name: str,
    queries: list[dict[str, object]],
    retriever,
    k: int = 4,
) -> RetrievalMetrics:
    """Evaluate retrieval for labeled queries."""
    accuracies: list[float] = []
    precisions: list[float] = []
    recalls: list[float] = []
    timings: list[float] = []

    for item in queries:
        query = str(item["query"])
        expected = set(item.get("expected_chunk_ids", []))
        started = time.perf_counter()
        chunks = retriever(query)
        timings.append(time.perf_counter() - started)
        retrieved_ids = [chunk.chunk_id for chunk in chunks]
        accuracies.append(retrieval_accuracy(retrieved_ids, expected, k))
        precisions.append(precision_at_k(retrieved_ids, expected, k))
        recalls.append(recall_at_k(retrieved_ids, expected, k))

    count = max(len(queries), 1)
    return RetrievalMetrics(
        retrieval_accuracy=sum(accuracies) / count,
        precision_at_k=sum(precisions) / count,
        recall_at_k=sum(recalls) / count,
        average_response_time=sum(timings) / count,
    )


def write_markdown_report(results: dict[str, RetrievalMetrics], path: Path) -> None:
    """Write a Markdown evaluation report."""
    lines = [
        "# DocSensei Evaluation Report",
        "",
        "| Strategy | Retrieval Accuracy | Precision@K | Recall@K | Avg Response Time |",
        "|---|---:|---:|---:|---:|",
    ]
    for strategy, metrics in results.items():
        lines.append(
            "| "
            f"{strategy} | {metrics.retrieval_accuracy:.3f} | "
            f"{metrics.precision_at_k:.3f} | {metrics.recall_at_k:.3f} | "
            f"{metrics.average_response_time:.3f}s |"
        )
    path.write_text("\n".join(lines), encoding="utf-8")
