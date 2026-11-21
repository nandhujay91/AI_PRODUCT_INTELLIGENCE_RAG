"""
Unit tests for ChromaDB metadata preparation.
"""

import pytest

from ai_product_intelligence_rag.documents.metadata_preparation import (
    prepare_chroma_metadata,
)


def test_prepare_valid_metadata() -> None:
    """Valid metadata should be preserved."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": 49.99,
        "average_rating": 4.5,
        "rating_number": 100,
        "store": "Example Store",
    }

    result = prepare_chroma_metadata(metadata)

    assert result == metadata


def test_remove_missing_optional_values() -> None:
    """None values should be omitted from prepared metadata."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": None,
        "average_rating": None,
        "rating_number": None,
    }

    result = prepare_chroma_metadata(metadata)

    assert "price" not in result
    assert "average_rating" not in result
    assert "rating_number" not in result


def test_preserve_boolean_metadata() -> None:
    """Boolean metadata should remain boolean."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "is_available": True,
    }

    result = prepare_chroma_metadata(metadata)

    assert result["is_available"] is True


def test_invalid_metadata_raises_error() -> None:
    """Invalid required metadata should raise a ValueError."""

    metadata = {
        "parent_asin": "",
        "title": "Wireless Headphones",
    }

    with pytest.raises(ValueError, match="Invalid product metadata"):
        prepare_chroma_metadata(metadata)


def test_invalid_price_raises_error() -> None:
    """Negative prices should not be prepared."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": -10.0,
    }

    with pytest.raises(ValueError):
        prepare_chroma_metadata(metadata)


def test_original_metadata_is_not_modified() -> None:
    """Preparation should not modify the original dictionary."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": None,
    }

    original_metadata = metadata.copy()

    prepare_chroma_metadata(metadata)

    assert metadata == original_metadata


def test_reject_nan_metadata() -> None:
    """NaN values should be rejected."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "discount": float("nan"),
    }

    with pytest.raises(ValueError, match="finite number"):
        prepare_chroma_metadata(metadata)


def test_reject_infinite_metadata() -> None:
    """Infinite numeric values should be rejected."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "discount": float("inf"),
    }

    with pytest.raises(ValueError, match="finite number"):
        prepare_chroma_metadata(metadata)


def test_reject_unsupported_metadata_type() -> None:
    """Unsupported Python objects should raise a ValueError."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "extra_data": {"color": "black"},
    }

    with pytest.raises(ValueError, match="Unsupported metadata type"):
        prepare_chroma_metadata(metadata)


def test_reject_empty_metadata_key() -> None:
    """Metadata keys must not be empty."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "": "invalid",
    }

    with pytest.raises(ValueError, match="non-empty strings"):
        prepare_chroma_metadata(metadata)


def test_reject_non_dictionary_metadata() -> None:
    """Metadata input must be a dictionary."""

    with pytest.raises(ValueError, match="must be a dictionary"):
        prepare_chroma_metadata(None)
