"""
Validate product metadata before vector database storage.
"""

from typing import Any


def validate_metadata(metadata: dict[str, Any]) -> list[str]:
    """
    Validate product metadata fields.

    Required fields:
        - parent_asin
        - title

    Optional fields:
        - price
        - average_rating
        - rating_number

    Returns:
        A list of validation errors. Empty means valid metadata.
    """

    errors = []

    product_id = metadata.get("parent_asin")
    title = metadata.get("title")
    price = metadata.get("price")
    average_rating = metadata.get("average_rating")
    rating_number = metadata.get("rating_number")

    # Validate product ID.
    if not isinstance(product_id, str) or not product_id.strip():
        errors.append("Missing or invalid product ID")

    # Validate product title.
    if not isinstance(title, str) or not title.strip():
        errors.append("Missing or invalid product title")

    # Validate price.
    if price is not None:
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            errors.append("Invalid product price")

    # Validate average rating.
    if average_rating is not None:
        if (
            isinstance(average_rating, bool)
            or not isinstance(average_rating, (int, float))
            or not 0 <= average_rating <= 5
        ):
            errors.append("Invalid average rating")

    # Validate rating count.
    if rating_number is not None:
        if (
            isinstance(rating_number, bool)
            or not isinstance(rating_number, int)
            or rating_number < 0
        ):
            errors.append("Invalid rating count")

    return errors
