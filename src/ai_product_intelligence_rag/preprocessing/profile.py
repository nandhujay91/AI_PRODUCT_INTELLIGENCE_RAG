"""
Profile a sample of Amazon product metadata.
"""

from collections.abc import Iterable
from itertools import islice
from statistics import mean, median


def parse_price(value: object) -> float | None:
    """Convert a valid price value into a number."""

    if not isinstance(value, (str, int, float)):
        return None

    if isinstance(value, str):
        cleaned_value = value.strip()

        if cleaned_value.lower() in {"", "none", "null", "n/a"}:
            return None

        cleaned_value = cleaned_value.replace(",", "")

        if cleaned_value.startswith("$"):
            cleaned_value = cleaned_value[1:].strip()

        value = cleaned_value

    try:
        price = float(value)
    except (ValueError, TypeError):
        return None

    if price < 0:
        return None

    return price


def profile_products(
    products: Iterable[dict],
    sample_size: int = 10000,
) -> dict:
    """Calculate detailed quality metrics for product records."""

    records = list(islice(products, sample_size))

    product_ids = [
        product.get("parent_asin") for product in records if product.get("parent_asin")
    ]

    prices = [
        price
        for product in records
        if (price := parse_price(product.get("price"))) is not None
    ]

    ratings = [
        product["average_rating"]
        for product in records
        if isinstance(product.get("average_rating"), (int, float))
    ]

    return {
        "total_sampled": len(records),
        "missing_titles": sum(not product.get("title") for product in records),
        "missing_prices": len(records) - len(prices),
        "missing_product_ids": sum(
            not product.get("parent_asin") for product in records
        ),
        "empty_descriptions": sum(
            not product.get("description") for product in records
        ),
        "empty_features": sum(not product.get("features") for product in records),
        "duplicate_product_ids": len(product_ids) - len(set(product_ids)),
        "valid_prices": len(prices),
        "price_min": min(prices) if prices else None,
        "price_max": max(prices) if prices else None,
        "price_average": round(mean(prices), 2) if prices else None,
        "price_median": median(prices) if prices else None,
        "rating_average": round(mean(ratings), 2) if ratings else None,
        "rating_median": median(ratings) if ratings else None,
    }
