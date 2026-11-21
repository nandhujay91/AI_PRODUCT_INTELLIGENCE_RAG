"""
Unit tests for Amazon product cleaning functions.
"""

from ai_product_intelligence_rag.preprocessing.cleaning import (
    clean_product,
    clean_product_description,
    clean_product_features,
    clean_product_id,
    clean_product_price,
    clean_product_title,
)


def test_clean_product_id_removes_whitespace() -> None:
    """Surrounding whitespace should be removed."""

    assert clean_product_id(" B001 ") == "B001"


def test_clean_product_id_preserves_valid_id() -> None:
    """A valid product ID should remain unchanged."""

    assert clean_product_id("B002") == "B002"


def test_clean_product_id_returns_none_for_empty_value() -> None:
    """An empty product ID should return None."""

    assert clean_product_id("   ") is None


def test_clean_product_id_returns_none_for_invalid_type() -> None:
    """A non-string product ID should return None."""

    assert clean_product_id(12345) is None


def test_clean_product_title_removes_whitespace() -> None:
    """Surrounding whitespace should be removed."""

    assert clean_product_title(" Wireless Headphones ") == "Wireless Headphones"


def test_clean_product_title_preserves_valid_title() -> None:
    """A valid title should remain unchanged."""

    assert clean_product_title("USB Keyboard") == "USB Keyboard"


def test_clean_product_title_returns_none_for_empty_value() -> None:
    """An empty title should return None."""

    assert clean_product_title("   ") is None


def test_clean_product_title_returns_none_for_invalid_type() -> None:
    """A non-string title should return None."""

    assert clean_product_title(12345) is None


def test_clean_product_price_converts_string() -> None:
    """A numeric string should become a float."""

    assert clean_product_price("19.99") == 19.99


def test_clean_product_price_handles_comma() -> None:
    """Thousands separators should be removed."""

    assert clean_product_price("1,299.99") == 1299.99


def test_clean_product_price_handles_missing_value() -> None:
    """Missing price values should return None."""

    assert clean_product_price("None") is None
    assert clean_product_price(None) is None
    assert clean_product_price("N/A") is None


def test_clean_product_price_rejects_invalid_value() -> None:
    """Invalid and negative prices should return None."""

    assert clean_product_price("invalid") is None
    assert clean_product_price("-10.00") is None
    assert clean_product_price(True) is None


def test_clean_product_description_from_list() -> None:
    """Description lists should be cleaned."""

    description = ["  Good sound quality  ", "Long battery life"]

    assert clean_product_description(description) == [
        "Good sound quality",
        "Long battery life",
    ]


def test_clean_product_description_from_string() -> None:
    """A single description string should become a list."""

    assert clean_product_description("  Wireless headphones  ") == [
        "Wireless headphones"
    ]


def test_clean_product_description_removes_empty_values() -> None:
    """Empty description elements should be removed."""

    assert clean_product_description(["", "  ", "Useful product"]) == ["Useful product"]


def test_clean_product_description_handles_missing_value() -> None:
    """Missing descriptions should return an empty list."""

    assert clean_product_description(None) == []
    assert clean_product_description([]) == []


def test_clean_product_features_from_list() -> None:
    """Feature lists should be cleaned."""

    features = ["  Noise cancellation  ", "Long battery life"]

    assert clean_product_features(features) == [
        "Noise cancellation",
        "Long battery life",
    ]


def test_clean_product_features_from_string() -> None:
    """A single feature string should become a list."""

    assert clean_product_features("  Bluetooth 5.0  ") == ["Bluetooth 5.0"]


def test_clean_product_features_removes_empty_values() -> None:
    """Empty feature elements should be removed."""

    assert clean_product_features(["", "  ", "Wireless"]) == ["Wireless"]


def test_clean_product_features_handles_missing_value() -> None:
    """Missing features should return an empty list."""

    assert clean_product_features(None) == []
    assert clean_product_features([]) == []


def test_clean_product() -> None:
    """All supported product fields should be cleaned consistently."""

    product = {
        "parent_asin": " B001 ",
        "title": " Wireless Headphones ",
        "price": "49.99",
        "description": [" Good sound quality ", ""],
        "features": [" Noise cancellation ", "Long battery life"],
        "average_rating": 4.5,
        "rating_number": 100,
        "main_category": "Electronics",
        "categories": ["Headphones"],
        "store": "Example Store",
    }

    cleaned_product = clean_product(product)

    assert cleaned_product == {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": 49.99,
        "description": ["Good sound quality"],
        "features": ["Noise cancellation", "Long battery life"],
        "average_rating": 4.5,
        "rating_number": 100,
        "main_category": "Electronics",
        "categories": ["Headphones"],
        "store": "Example Store",
    }


def test_clean_product_preserves_missing_optional_fields() -> None:
    """Missing optional fields should receive consistent defaults."""

    product = {
        "parent_asin": "B002",
        "title": "USB Keyboard",
        "price": "None",
    }

    cleaned_product = clean_product(product)

    assert cleaned_product["price"] is None
    assert cleaned_product["description"] == []
    assert cleaned_product["features"] == []
    assert cleaned_product["average_rating"] is None
    assert cleaned_product["rating_number"] is None
