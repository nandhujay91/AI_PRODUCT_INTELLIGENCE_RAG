"""
Generate quality metrics for product documents before embedding.
"""

from collections.abc import Iterable
from typing import Any

from ai_product_intelligence_rag.documents.document_quality import (
    count_duplicate_documents,
    is_document_empty,
    is_document_low_information,
)


def generate_document_quality_report(
    documents: Iterable[dict[str, Any]],
    min_length: int = 30,
) -> dict[str, int]:
    """
    Calculate quality metrics for a collection of product documents.

    Args:
        documents: Product documents containing page_content and metadata.
        min_length: Minimum content length for a document.

    Returns:
        A dictionary containing document quality metrics.
    """

    total_documents = 0
    empty_documents = 0
    low_information_documents = 0

    document_list = list(documents)

    for document in document_list:
        total_documents += 1

        page_content = document.get("page_content")

        if is_document_empty(page_content):
            empty_documents += 1
            continue

        if is_document_low_information(page_content, min_length):
            low_information_documents += 1

    duplicate_documents = count_duplicate_documents(document_list)

    rejected_documents = empty_documents + low_information_documents

    suitable_documents = total_documents - rejected_documents

    return {
        "total_documents": total_documents,
        "empty_documents": empty_documents,
        "low_information_documents": low_information_documents,
        "duplicate_documents": duplicate_documents,
        "suitable_documents": suitable_documents,
    }
