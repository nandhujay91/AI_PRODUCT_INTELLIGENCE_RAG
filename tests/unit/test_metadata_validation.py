"""
Unit tests for product metadata validation.
"""

from ai_product_intelligence_rag.documents.metadata_validation import (
    validate_metadata,
)


def test_valid_metadata() -> None:
    """Complete required metadata should pass."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
    }

    assert validate_metadata(metadata) == []


def test_missing_product_id() -> None:
    """Missing product ID should produce a validation error."""

    metadata = {
        "parent_asin": "",
        "title": "Wireless Headphones",
    }

    errors = validate_metadata(metadata)

    assert "Missing or invalid product ID" in errors


def test_missing_title() -> None:
    """Missing title should produce a validation error."""

    metadata = {
        "parent_asin": "B001",
        "title": "",
    }

    errors = validate_metadata(metadata)

    assert "Missing or invalid product title" in errors


def test_missing_all_required_fields() -> None:
    """Both required fields should be reported when missing."""

    errors = validate_metadata({})

    assert len(errors) == 2


def test_invalid_metadata_types() -> None:
    """Non-string required fields should be rejected."""

    metadata = {
        "parent_asin": 123,
        "title": None,
    }

    errors = validate_metadata(metadata)

    assert len(errors) == 2


def test_valid_price_and_rating_metadata() -> None:
    """Valid price and rating values should pass."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": 49.99,
        "average_rating": 4.5,
        "rating_number": 100,
    }

    assert validate_metadata(metadata) == []


def test_missing_optional_metadata() -> None:
    """Missing optional values should be allowed."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": None,
        "average_rating": None,
        "rating_number": None,
    }

    assert validate_metadata(metadata) == []


def test_invalid_price() -> None:
    """Negative or non-numeric prices should be rejected."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": -10.0,
    }

    assert "Invalid product price" in validate_metadata(metadata)


def test_invalid_average_rating() -> None:
    """Ratings outside the zero-to-five range should be rejected."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "average_rating": 6.0,
    }

    assert "Invalid average rating" in validate_metadata(metadata)


def test_invalid_rating_count() -> None:
    """Negative or non-integer rating counts should be rejected."""

    metadata = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "rating_number": -5,
    }

    assert "Invalid rating count" in validate_metadata(metadata)
