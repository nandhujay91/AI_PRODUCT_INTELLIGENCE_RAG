"""
Generate data-quality metrics for Amazon product records.
"""

from collections import Counter
from collections.abc import Iterable
from typing import Any


def generate_quality_report(
    products: Iterable[dict[str, Any]],
) -> dict[str, int]:
    """
    Calculate basic data-quality metrics for product records.

    Args:
        products: An iterable of Amazon product records.

    Returns:
        A dictionary containing data-quality metrics.
    """

    total_records = 0
    missing_product_ids = 0
    missing_titles = 0
    missing_prices = 0
    missing_descriptions = 0
    missing_features = 0

    product_ids = []

    for product in products:
        total_records += 1

        product_id = product.get("parent_asin")
        title = product.get("title")
        price = product.get("price")
        description = product.get("description")
        features = product.get("features")

        if not isinstance(product_id, str) or not product_id.strip():
            missing_product_ids += 1
        else:
            product_ids.append(product_id.strip())

        if not isinstance(title, str) or not title.strip():
            missing_titles += 1

        if price is None or str(price).strip().lower() in {
            "",
            "none",
            "null",
            "n/a",
        }:
            missing_prices += 1

        if not description:
            missing_descriptions += 1

        if not features:
            missing_features += 1

    duplicate_product_ids = sum(
        count - 1 for count in Counter(product_ids).values() if count > 1
    )

    return {
        "total_records": total_records,
        "missing_product_ids": missing_product_ids,
        "missing_titles": missing_titles,
        "missing_prices": missing_prices,
        "missing_descriptions": missing_descriptions,
        "missing_features": missing_features,
        "duplicate_product_ids": duplicate_product_ids,
    }


def merge_quality_reports(
    reports: Iterable[dict[str, int]],
) -> dict[str, int]:
    """
    Combine quality metrics from multiple batches.

    Duplicate IDs are counted within each batch only.
    """

    metric_names = (
        "total_records",
        "missing_product_ids",
        "missing_titles",
        "missing_prices",
        "missing_descriptions",
        "missing_features",
        "duplicate_product_ids",
    )

    combined_report = dict.fromkeys(metric_names, 0)

    for report in reports:
        for metric in metric_names:
            combined_report[metric] += report[metric]

    return combined_report


def count_cross_batch_duplicates(
    batches: Iterable[Iterable[dict[str, Any]]],
) -> int:
    """
    Count duplicate product IDs across multiple batches.

    Only valid, non-empty product IDs are considered.
    """

    seen_product_ids = set()
    duplicate_count = 0

    for batch in batches:
        for product in batch:
            product_id = product.get("parent_asin")

            if not isinstance(product_id, str) or not product_id.strip():
                continue

            normalized_id = product_id.strip()

            if normalized_id in seen_product_ids:
                duplicate_count += 1
            else:
                seen_product_ids.add(normalized_id)

    return duplicate_count
