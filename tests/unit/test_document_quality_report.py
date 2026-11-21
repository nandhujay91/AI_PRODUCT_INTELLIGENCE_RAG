"""
Unit tests for product document quality reporting.
"""

from ai_product_intelligence_rag.documents.document_quality_report import (
    generate_document_quality_report,
)


def test_document_quality_report_with_valid_documents() -> None:
    """Valid documents should be classified as suitable."""

    documents = [
        {"page_content": "Wireless headphones with noise cancellation."},
        {"page_content": "Mechanical keyboard with USB connectivity."},
    ]

    report = generate_document_quality_report(documents)

    assert report["total_documents"] == 2
    assert report["empty_documents"] == 0
    assert report["low_information_documents"] == 0
    assert report["duplicate_documents"] == 0
    assert report["suitable_documents"] == 2


def test_document_quality_report_with_empty_documents() -> None:
    """Empty documents should be counted correctly."""

    documents = [
        {"page_content": ""},
        {"page_content": "   "},
        {"page_content": "Wireless headphones with noise cancellation."},
    ]

    report = generate_document_quality_report(documents)

    assert report["total_documents"] == 3
    assert report["empty_documents"] == 2
    assert report["low_information_documents"] == 0
    assert report["suitable_documents"] == 1


def test_document_quality_report_with_low_information() -> None:
    """Short documents should be classified as low-information."""

    documents = [
        {"page_content": "USB mouse"},
        {"page_content": "Wireless headphones with noise cancellation."},
    ]

    report = generate_document_quality_report(documents)

    assert report["total_documents"] == 2
    assert report["empty_documents"] == 0
    assert report["low_information_documents"] == 1
    assert report["suitable_documents"] == 1


def test_document_quality_report_with_duplicates() -> None:
    """Duplicate documents should be counted separately."""

    documents = [
        {"page_content": "Wireless headphones with noise cancellation."},
        {"page_content": "USB keyboard with wireless connectivity."},
        {"page_content": "Wireless headphones with noise cancellation."},
    ]

    report = generate_document_quality_report(documents)

    assert report["total_documents"] == 3
    assert report["duplicate_documents"] == 1
    assert report["suitable_documents"] == 3


def test_document_quality_report_with_custom_minimum_length() -> None:
    """A custom minimum length should be applied."""

    documents = [
        {"page_content": "Wireless headphones"},
    ]

    report = generate_document_quality_report(
        documents,
        min_length=30,
    )

    assert report["low_information_documents"] == 1
    assert report["suitable_documents"] == 0


def test_document_quality_report_with_empty_input() -> None:
    """An empty collection should return zero metrics."""

    report = generate_document_quality_report([])

    assert report == {
        "total_documents": 0,
        "empty_documents": 0,
        "low_information_documents": 0,
        "duplicate_documents": 0,
        "suitable_documents": 0,
    }
