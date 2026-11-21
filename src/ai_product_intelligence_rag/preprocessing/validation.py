"""
Validation rules for Amazon product records.
"""

from ai_product_intelligence_rag.preprocessing.profile import parse_price

MIN_RATING = 0
MAX_RATING = 5

MISSING_PRICE_VALUES = {"", "none", "null", "n/a"}


def validate_product_id(product_id: object) -> bool:
    """Check whether a product ID is valid."""

    return isinstance(product_id, str) and bool(product_id.strip())


def validate_title(title: object) -> bool:
    """Check whether a product title is valid."""

    return isinstance(title, str) and bool(title.strip())


def validate_price(price: object) -> bool:
    """
    Check whether a product price is valid or legitimately missing.

    Missing prices are allowed. Invalid non-missing prices are rejected.
    """

    if price is None:
        return True

    if isinstance(price, str):
        if price.strip().lower() in MISSING_PRICE_VALUES:
            return True

    return parse_price(price) is not None


def validate_rating(rating: object) -> bool:
    """Check whether a product rating is between zero and five."""

    if rating is None:
        return True

    if isinstance(rating, bool) or not isinstance(rating, (int, float)):
        return False

    return MIN_RATING <= rating <= MAX_RATING


def validate_rating_count(rating_count: object) -> bool:
    """Check whether the number of ratings is non-negative."""

    if rating_count is None:
        return True

    if isinstance(rating_count, bool):
        return False

    if not isinstance(rating_count, (int, float)):
        return False

    return rating_count >= 0


def validate_product(product: dict) -> list[str]:
    """
    Validate one Amazon product record.

    Returns:
        A list of validation errors.
        An empty list means the product passed validation.
    """

    errors = []

    if not validate_product_id(product.get("parent_asin")):
        errors.append("Missing or invalid product ID")

    if not validate_title(product.get("title")):
        errors.append("Missing or invalid product title")

    if not validate_price(product.get("price")):
        errors.append("Invalid product price")

    if not validate_rating(product.get("average_rating")):
        errors.append("Product rating must be between 0 and 5")

    if not validate_rating_count(product.get("rating_number")):
        errors.append("Invalid rating count")

    return errors
