"""Tests for product document length statistics."""

from ai_product_intelligence_rag.documents.document_statistics import (
    calculate_document_statistics,
)


def test_calculate_document_statistics() -> None:
    """Calculate statistics for documents with different lengths."""

    documents = [
        {"page_content": "A" * 100},
        {"page_content": "B" * 200},
        {"page_content": "C" * 300},
        {"page_content": "D" * 400},
    ]

    result = calculate_document_statistics(documents)

    assert result["total_documents"] == 4
    assert result["empty_documents"] == 0
    assert result["minimum_length"] == 100
    assert result["maximum_length"] == 400
    assert result["average_length"] == 250
    assert result["median_length"] == 250


def test_empty_documents_are_excluded_from_length_statistics() -> None:
    """Empty documents should not affect non-empty length calculations."""

    documents = [
        {"page_content": "A" * 100},
        {"page_content": ""},
        {"page_content": "B" * 200},
    ]

    result = calculate_document_statistics(documents)

    assert result["total_documents"] == 3
    assert result["empty_documents"] == 1
    assert result["minimum_length"] == 100
    assert result["maximum_length"] == 200
    assert result["average_length"] == 150


def test_all_documents_empty() -> None:
    """Handle a collection containing only empty documents."""

    documents = [
        {"page_content": ""},
        {"page_content": "   "},
    ]

    result = calculate_document_statistics(documents)

    assert result["total_documents"] == 2
    assert result["empty_documents"] == 2
    assert result["minimum_length"] == 0
    assert result["maximum_length"] == 0
    assert result["average_length"] == 0.0


def test_empty_input() -> None:
    """Handle an empty document collection."""

    result = calculate_document_statistics([])

    assert result["total_documents"] == 0
    assert result["empty_documents"] == 0
    assert result["minimum_length"] == 0
    assert result["maximum_length"] == 0


def test_missing_page_content() -> None:
    """Treat missing page content as an empty document."""

    documents = [
        {"metadata": {"parent_asin": "B001"}},
        {"page_content": "Product title"},
    ]

    result = calculate_document_statistics(documents)

    assert result["total_documents"] == 2
    assert result["empty_documents"] == 1
    assert result["minimum_length"] == 13


def test_percentile_calculations() -> None:
    """Calculate the 90th and 95th percentiles."""

    documents = [{"page_content": "A" * length} for length in range(100, 1100, 100)]

    result = calculate_document_statistics(documents)

    assert result["p90_length"] == 910
    assert result["p95_length"] == 955
