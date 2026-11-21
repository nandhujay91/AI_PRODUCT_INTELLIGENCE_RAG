"""
Calculate text-length statistics for product documents.
"""

from collections.abc import Iterable
from typing import Any

import numpy as np


def calculate_document_statistics(
    documents: Iterable[dict[str, Any]],
) -> dict[str, int | float]:
    """
    Calculate document length statistics using character counts.

    Args:
        documents: Product documents containing page_content.

    Returns:
        Summary statistics for document lengths.
    """

    lengths = []

    for document in documents:
        page_content = document.get("page_content", "")

        if isinstance(page_content, str):
            lengths.append(len(page_content.strip()))

    if not lengths:
        return {
            "total_documents": 0,
            "empty_documents": 0,
            "minimum_length": 0,
            "maximum_length": 0,
            "average_length": 0.0,
            "median_length": 0.0,
            "p90_length": 0.0,
            "p95_length": 0.0,
        }

    non_empty_lengths = [length for length in lengths if length > 0]

    if not non_empty_lengths:
        return {
            "total_documents": len(lengths),
            "empty_documents": len(lengths),
            "minimum_length": 0,
            "maximum_length": 0,
            "average_length": 0.0,
            "median_length": 0.0,
            "p90_length": 0.0,
            "p95_length": 0.0,
        }

    return {
        "total_documents": len(lengths),
        "empty_documents": lengths.count(0),
        "minimum_length": min(non_empty_lengths),
        "maximum_length": max(non_empty_lengths),
        "average_length": round(float(np.mean(non_empty_lengths)), 2),
        "median_length": round(float(np.median(non_empty_lengths)), 2),
        "p90_length": round(float(np.percentile(non_empty_lengths, 90)), 2),
        "p95_length": round(float(np.percentile(non_empty_lengths, 95)), 2),
    }
