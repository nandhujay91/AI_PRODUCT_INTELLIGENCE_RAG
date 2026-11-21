"""
Unit tests for Amazon product data-quality reporting.
"""

from ai_product_intelligence_rag.preprocessing.quality_report import (
    count_cross_batch_duplicates,
    generate_quality_report,
    merge_quality_reports,
)


def test_quality_report_with_complete_products() -> None:
    """Complete products should have no missing fields or duplicates."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "description": ["Bluetooth headphones"],
            "features": ["Noise cancellation"],
        },
        {
            "parent_asin": "B002",
            "title": "USB Keyboard",
            "price": "29.99",
            "description": ["USB keyboard"],
            "features": ["Wireless"],
        },
    ]

    report = generate_quality_report(products)

    assert report["total_records"] == 2
    assert report["missing_product_ids"] == 0
    assert report["missing_titles"] == 0
    assert report["missing_prices"] == 0
    assert report["missing_descriptions"] == 0
    assert report["missing_features"] == 0
    assert report["duplicate_product_ids"] == 0


def test_quality_report_with_missing_values() -> None:
    """Missing product information should be counted correctly."""

    products = [
        {
            "parent_asin": "",
            "title": "",
            "price": "None",
            "description": [],
            "features": [],
        }
    ]

    report = generate_quality_report(products)

    assert report["total_records"] == 1
    assert report["missing_product_ids"] == 1
    assert report["missing_titles"] == 1
    assert report["missing_prices"] == 1
    assert report["missing_descriptions"] == 1
    assert report["missing_features"] == 1


def test_quality_report_with_duplicate_ids() -> None:
    """Repeated product IDs should be counted."""

    products = [
        {"parent_asin": "B001", "title": "Product A"},
        {"parent_asin": "B001", "title": "Product A"},
        {"parent_asin": "B002", "title": "Product B"},
    ]

    report = generate_quality_report(products)

    assert report["duplicate_product_ids"] == 1


def test_quality_report_with_empty_input() -> None:
    """An empty input should return zero metrics."""

    report = generate_quality_report([])

    assert report == {
        "total_records": 0,
        "missing_product_ids": 0,
        "missing_titles": 0,
        "missing_prices": 0,
        "missing_descriptions": 0,
        "missing_features": 0,
        "duplicate_product_ids": 0,
    }


def test_merge_quality_reports() -> None:
    """Metrics from multiple batches should be combined."""

    reports = [
        {
            "total_records": 100,
            "missing_product_ids": 2,
            "missing_titles": 1,
            "missing_prices": 20,
            "missing_descriptions": 30,
            "missing_features": 10,
            "duplicate_product_ids": 1,
        },
        {
            "total_records": 50,
            "missing_product_ids": 1,
            "missing_titles": 0,
            "missing_prices": 10,
            "missing_descriptions": 15,
            "missing_features": 5,
            "duplicate_product_ids": 0,
        },
    ]

    report = merge_quality_reports(reports)

    assert report["total_records"] == 150
    assert report["missing_product_ids"] == 3
    assert report["missing_prices"] == 30
    assert report["duplicate_product_ids"] == 1


def test_cross_batch_duplicate_ids() -> None:
    """Detect the same product ID appearing in different batches."""

    batches = [
        [{"parent_asin": "B001"}, {"parent_asin": "B002"}],
        [{"parent_asin": "B003"}, {"parent_asin": "B001"}],
    ]

    assert count_cross_batch_duplicates(batches) == 1


def test_cross_batch_without_duplicates() -> None:
    """Different product IDs across batches should have no duplicates."""

    batches = [
        [{"parent_asin": "B001"}, {"parent_asin": "B002"}],
        [{"parent_asin": "B003"}, {"parent_asin": "B004"}],
    ]

    assert count_cross_batch_duplicates(batches) == 0


def test_cross_batch_multiple_occurrences() -> None:
    """Count every repeated occurrence after the first."""

    batches = [
        [{"parent_asin": "B001"}],
        [{"parent_asin": "B001"}],
        [{"parent_asin": "B001"}],
    ]

    assert count_cross_batch_duplicates(batches) == 2


def test_cross_batch_ignores_invalid_ids() -> None:
    """Missing and invalid product IDs should be ignored."""

    batches = [
        [{"parent_asin": None}, {"parent_asin": ""}],
        [{"parent_asin": "B001"}, {"parent_asin": None}],
    ]

    assert count_cross_batch_duplicates(batches) == 0


def test_cross_batch_normalizes_product_ids() -> None:
    """Whitespace around product IDs should not hide duplicates."""

    batches = [
        [{"parent_asin": " B001 "}],
        [{"parent_asin": "B001"}],
    ]

    assert count_cross_batch_duplicates(batches) == 1
