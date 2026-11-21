"""
Unit tests for product document quality validation.
"""

import pytest

from ai_product_intelligence_rag.documents.document_quality import (
    count_duplicate_documents,
    is_document_empty,
    is_document_low_information,
)


def test_document_with_content_is_not_empty() -> None:
    """A document containing text should not be empty."""

    assert is_document_empty("Wireless Headphones") is False


def test_empty_document() -> None:
    """An empty string should be detected."""

    assert is_document_empty("") is True


def test_whitespace_document() -> None:
    """Whitespace-only content should be detected."""

    assert is_document_empty("   ") is True


def test_none_document() -> None:
    """None should be treated as empty."""

    assert is_document_empty(None) is True


def test_invalid_document_type() -> None:
    """Non-string document content should be treated as invalid."""

    assert is_document_empty(123) is True


def test_low_information_document() -> None:
    """Text shorter than the minimum length should be flagged."""

    assert is_document_low_information("USB mouse") is True


def test_document_at_minimum_length() -> None:
    """Text exactly at the minimum length should pass."""

    content = "A" * 30

    assert is_document_low_information(content) is False


def test_document_above_minimum_length() -> None:
    """Text longer than the minimum length should pass."""

    content = "Wireless headphones with noise cancellation."

    assert is_document_low_information(content) is False


def test_custom_minimum_length() -> None:
    """A custom minimum length should be supported."""

    assert (
        is_document_low_information(
            "Wireless headphones",
            min_length=10,
        )
        is False
    )


def test_invalid_minimum_length() -> None:
    """A non-positive minimum length should raise a ValueError."""

    with pytest.raises(ValueError):
        is_document_low_information(
            "Wireless headphones",
            min_length=0,
        )


def test_empty_content_is_low_information() -> None:
    """Empty content should also be considered low-information."""

    assert is_document_low_information("") is True


def test_count_duplicate_documents() -> None:
    """Identical document contents should be counted as duplicates."""

    documents = [
        {"page_content": "Wireless Bluetooth Headphones"},
        {"page_content": "USB Keyboard"},
        {"page_content": "Wireless Bluetooth Headphones"},
    ]

    assert count_duplicate_documents(documents) == 1


def test_count_multiple_duplicate_documents() -> None:
    """Every repeated occurrence after the first should be counted."""

    documents = [
        {"page_content": "Wireless Headphones"},
        {"page_content": "Wireless Headphones"},
        {"page_content": "Wireless Headphones"},
    ]

    assert count_duplicate_documents(documents) == 2


def test_count_duplicate_documents_with_whitespace() -> None:
    """Surrounding whitespace should not hide identical documents."""

    documents = [
        {"page_content": " Wireless Headphones "},
        {"page_content": "Wireless Headphones"},
    ]

    assert count_duplicate_documents(documents) == 1


def test_count_duplicate_documents_ignores_empty_content() -> None:
    """Empty documents should not be counted as duplicates."""

    documents = [
        {"page_content": ""},
        {"page_content": "   "},
        {"page_content": "Wireless Headphones"},
    ]

    assert count_duplicate_documents(documents) == 0


def test_count_duplicate_documents_empty_input() -> None:
    """An empty document collection should return zero duplicates."""

    assert count_duplicate_documents([]) == 0


def test_low_information_rejects_invalid_min_length_for_empty_document() -> None:
    """Invalid minimum length should raise even for empty content."""

    with pytest.raises(ValueError):
        is_document_low_information("", min_length=0)
