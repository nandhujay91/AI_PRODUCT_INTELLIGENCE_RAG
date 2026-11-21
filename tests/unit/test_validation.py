"""
Tests for Amazon product validation.
"""

from ai_product_intelligence_rag.preprocessing.validation import (
    validate_product,
)


def test_valid_product() -> None:
    """A complete product should pass validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 4.5,
        "rating_number": 100,
    }

    assert validate_product(product) == []


def test_missing_product_id() -> None:
    """A product without an ID should fail validation."""

    product = {
        "parent_asin": "",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 4.5,
    }

    errors = validate_product(product)

    assert "Missing or invalid product ID" in errors


def test_missing_price_is_allowed() -> None:
    """A product without a price should remain valid."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "None",
        "average_rating": 4.5,
    }

    assert validate_product(product) == []


def test_invalid_rating() -> None:
    """A rating above five should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 6,
    }

    errors = validate_product(product)

    assert "Product rating must be between 0 and 5" in errors


def test_missing_title() -> None:
    """A product without a title should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "",
        "price": "19.99",
        "average_rating": 4.5,
    }

    errors = validate_product(product)

    assert "Missing or invalid product title" in errors


def test_invalid_price() -> None:
    """A non-numeric price should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "invalid",
        "average_rating": 4.5,
    }

    errors = validate_product(product)

    assert "Invalid product price" in errors


def test_negative_rating() -> None:
    """A negative rating should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": -1,
    }

    errors = validate_product(product)

    assert "Product rating must be between 0 and 5" in errors


def test_rating_above_five() -> None:
    """A rating above five should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 6,
    }

    errors = validate_product(product)

    assert "Product rating must be between 0 and 5" in errors


def test_negative_rating_count() -> None:
    """A negative rating count should fail validation."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 4.5,
        "rating_number": -10,
    }

    errors = validate_product(product)

    assert "Invalid rating count" in errors


def test_missing_description_is_allowed() -> None:
    """A missing description should not invalidate a product."""

    product = {
        "parent_asin": "B07SM135LS",
        "title": "Laptop Protective Skin",
        "price": "19.99",
        "average_rating": 4.5,
        "description": None,
    }

    assert validate_product(product) == []
