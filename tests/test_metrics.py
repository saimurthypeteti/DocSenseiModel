from evaluation.metrics import precision_at_k, recall_at_k, retrieval_accuracy


def test_retrieval_metrics():
    retrieved = ["c1", "c2", "c3"]
    expected = {"c2", "c4"}

    assert precision_at_k(retrieved, expected, 2) == 0.5
    assert recall_at_k(retrieved, expected, 3) == 0.5
    assert retrieval_accuracy(retrieved, expected, 2) == 1.0
