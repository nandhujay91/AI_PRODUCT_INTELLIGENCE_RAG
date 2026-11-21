"""
Cleaning and normalization functions for Amazon product records.
"""

from collections.abc import Iterable
from typing import Any


def clean_product_id(product_id: object) -> str | None:
    """
    Normalize a product ID by removing surrounding whitespace.

    Returns:
        A cleaned product ID, or None if the value is missing or invalid.
    """

    if not isinstance(product_id, str):
        return None

    cleaned_id = product_id.strip()

    if not cleaned_id:
        return None

    return cleaned_id


def clean_product_title(title: object) -> str | None:
    """
    Normalize a product title by removing surrounding whitespace.

    Returns:
        A cleaned title, or None if the value is missing or invalid.
    """

    if not isinstance(title, str):
        return None

    cleaned_title = title.strip()

    if not cleaned_title:
        return None

    return cleaned_title


def clean_product_price(price: object) -> float | None:
    """
    Convert a product price into a numeric value.

    Returns:
        A non-negative numeric price, or None for missing or invalid values.
    """

    if price is None:
        return None

    if isinstance(price, bool):
        return None

    if isinstance(price, str):
        cleaned_price = price.strip().replace(",", "")

        if cleaned_price.lower() in {"", "none", "null", "n/a"}:
            return None

    else:
        cleaned_price = price

    try:
        numeric_price = float(cleaned_price)
    except (TypeError, ValueError):
        return None

    if numeric_price < 0:
        return None

    return numeric_price


def clean_product_description(description: object) -> list[str]:
    """
    Normalize product descriptions into a list of non-empty strings.
    """

    if isinstance(description, str):
        description_items = [description]
    elif isinstance(description, Iterable):
        if isinstance(description, (dict, bytes)):
            return []

        description_items = description
    else:
        return []

    cleaned_descriptions = []

    for item in description_items:
        if isinstance(item, str):
            cleaned_item = item.strip()

            if cleaned_item:
                cleaned_descriptions.append(cleaned_item)

    return cleaned_descriptions


def clean_product_features(features: object) -> list[str]:
    """
    Normalize product features into a list of non-empty strings.
    """

    if isinstance(features, str):
        feature_items = [features]
    elif isinstance(features, Iterable):
        if isinstance(features, (dict, bytes)):
            return []

        feature_items = features
    else:
        return []

    cleaned_features = []

    for item in feature_items:
        if isinstance(item, str):
            cleaned_item = item.strip()

            if cleaned_item:
                cleaned_features.append(cleaned_item)

    return cleaned_features


def clean_product(product: dict[str, Any]) -> dict[str, Any]:
    """
    Clean the supported fields of a validated Amazon product.

    Args:
        product: A product record that has passed validation.

    Returns:
        A standardized product record.
    """

    return {
        "parent_asin": clean_product_id(product.get("parent_asin")),
        "title": clean_product_title(product.get("title")),
        "price": clean_product_price(product.get("price")),
        "description": clean_product_description(product.get("description")),
        "features": clean_product_features(product.get("features")),
        "average_rating": product.get("average_rating"),
        "rating_number": product.get("rating_number"),
        "main_category": product.get("main_category"),
        "categories": product.get("categories"),
        "store": product.get("store"),
    }
