"""
Unit tests for the Amazon product processing pipeline.
"""

from typing import Any

import pytest

from ai_product_intelligence_rag.preprocessing import product_pipeline
from ai_product_intelligence_rag.preprocessing.product_pipeline import (
    process_product_batch,
    run_product_pipeline,
    stream_product_batches,
)


def test_process_valid_products() -> None:
    """Valid products should be accepted."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "average_rating": 4.5,
            "rating_number": 100,
        }
    ]

    results = process_product_batch(products)

    assert len(results["valid_products"]) == 1
    assert results["rejected_products"] == []


def test_reject_invalid_products() -> None:
    """Products with invalid required fields should be rejected."""

    products = [
        {
            "parent_asin": "",
            "title": "Wireless Headphones",
            "price": "49.99",
            "average_rating": 4.5,
            "rating_number": 100,
        }
    ]

    results = process_product_batch(products)

    assert results["valid_products"] == []
    assert len(results["rejected_products"]) == 1


def test_process_mixed_products() -> None:
    """The pipeline should separate valid and invalid products."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "average_rating": 4.5,
            "rating_number": 100,
        },
        {
            "parent_asin": "",
            "title": "Invalid Product",
            "price": "29.99",
            "average_rating": 4.0,
            "rating_number": 50,
        },
    ]

    results = process_product_batch(products)

    assert len(results["valid_products"]) == 1
    assert len(results["rejected_products"]) == 1


def test_process_empty_batch() -> None:
    """An empty batch should return empty results."""

    results = process_product_batch([])

    assert results["valid_products"] == []
    assert results["rejected_products"] == []


def test_stream_product_batches() -> None:
    """Products should be divided into batches of the requested size."""

    products = [{"id": number} for number in range(5)]

    batches = list(stream_product_batches(products, batch_size=2))

    assert [len(batch) for batch in batches] == [2, 2, 1]


def test_stream_product_batches_empty_input() -> None:
    """An empty input should produce no batches."""

    batches = list(stream_product_batches([], batch_size=2))

    assert batches == []


def test_stream_product_batches_invalid_size() -> None:
    """A non-positive batch size should raise a ValueError."""

    with pytest.raises(ValueError):
        list(stream_product_batches([], batch_size=0))


def test_run_product_pipeline(monkeypatch: pytest.MonkeyPatch) -> None:
    """The pipeline should process records and collect quality metrics."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "average_rating": 4.5,
            "rating_number": 100,
            "description": ["Bluetooth headphones"],
            "features": ["Noise cancellation"],
        },
        {
            "parent_asin": "",
            "title": "Invalid Product",
            "price": "29.99",
            "average_rating": 4.0,
            "rating_number": 50,
            "description": [],
            "features": [],
        },
        {
            "parent_asin": "B003",
            "title": "USB Keyboard",
            "price": "29.99",
            "average_rating": 4.2,
            "rating_number": 80,
            "description": ["USB keyboard"],
            "features": ["Wireless"],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=3, batch_size=2)

    assert results["total_processed"] == 3
    assert results["total_valid"] == 2
    assert results["total_rejected"] == 1
    assert results["quality_report"]["total_records"] == 3
    assert results["quality_report"]["missing_product_ids"] == 1
    assert results["quality_report"]["missing_descriptions"] == 1
    assert results["quality_report"]["missing_features"] == 1


def test_run_product_pipeline_combines_batch_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Quality metrics should be combined across multiple batches."""

    products = [
        {
            "parent_asin": f"B00{number}",
            "title": f"Product {number}",
            "price": "19.99",
            "description": ["Product description"],
            "features": ["Product feature"],
        }
        for number in range(1, 4)
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=3, batch_size=1)

    assert results["total_processed"] == 3
    assert results["quality_report"]["total_records"] == 3
    assert results["quality_report"]["missing_prices"] == 0
    assert results["quality_report"]["missing_product_ids"] == 0


def test_run_product_pipeline_invalid_sample_size() -> None:
    """A non-positive sample size should raise a ValueError."""

    with pytest.raises(ValueError):
        run_product_pipeline(sample_size=0, batch_size=100)


def test_process_product_batch_cleans_valid_products() -> None:
    """Valid products should be cleaned before being returned."""

    product = {
        "parent_asin": " B001 ",
        "title": " Wireless Headphones ",
        "price": "49.99",
        "average_rating": 4.5,
        "rating_number": 100,
        "description": [" Good sound quality "],
        "features": [" Noise cancellation "],
    }

    results = process_product_batch([product])

    cleaned_product = results["valid_products"][0]

    assert cleaned_product["parent_asin"] == "B001"
    assert cleaned_product["title"] == "Wireless Headphones"
    assert cleaned_product["price"] == 49.99
    assert cleaned_product["description"] == ["Good sound quality"]
    assert cleaned_product["features"] == ["Noise cancellation"]


def test_process_product_batch_preserves_raw_product() -> None:
    """Cleaning should not modify the original raw product."""

    product = {
        "parent_asin": " B001 ",
        "title": " Wireless Headphones ",
        "price": "49.99",
        "average_rating": 4.5,
        "rating_number": 100,
    }

    original_product = product.copy()

    process_product_batch([product])

    assert product == original_product


def test_run_product_pipeline_detects_cross_batch_duplicates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The pipeline should detect duplicate IDs across separate batches."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "description": ["Good sound quality"],
            "features": ["Noise cancellation"],
        },
        {
            "parent_asin": "B002",
            "title": "USB Keyboard",
            "price": "29.99",
            "description": ["USB keyboard"],
            "features": ["Wireless"],
        },
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
            "description": ["Good sound quality"],
            "features": ["Noise cancellation"],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(
        sample_size=3,
        batch_size=2,
    )

    assert results["total_processed"] == 3
    assert results["total_valid"] == 3
    assert results["total_rejected"] == 0
    assert results["quality_report"]["duplicate_product_ids"] == 1


def test_run_product_pipeline_counts_duplicates_correctly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Duplicates within and across batches should not be double-counted."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
        },
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
        },
        {
            "parent_asin": "B002",
            "title": "USB Keyboard",
            "price": "29.99",
        },
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones",
            "price": "49.99",
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(
        sample_size=4,
        batch_size=3,
    )

    assert results["quality_report"]["duplicate_product_ids"] == 2


def test_pipeline_generates_embedding_ready_documents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Valid products should generate embedding-ready documents."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "price": "49.99",
            "description": ["High quality wireless audio"],
            "features": ["Noise cancellation", "Bluetooth connectivity"],
        },
        {
            "parent_asin": "B002",
            "title": "Mechanical Keyboard with USB Connectivity",
            "price": "29.99",
            "description": ["Mechanical keyboard for professional use"],
            "features": ["USB connectivity"],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=2, batch_size=1)

    assert results["total_processed"] == 2
    assert results["total_valid"] == 2
    assert results["total_rejected"] == 0
    assert results["total_documents_created"] == 2
    assert len(results["embedding_ready_documents"]) == 2
    assert results["metadata_preparation_failures"] == 0

    assert results["document_quality_report"]["total_documents"] == 2
    assert results["document_quality_report"]["suitable_documents"] == 2


def test_pipeline_excludes_low_information_documents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Low-information documents should not be embedding-ready."""

    products = [
        {
            "parent_asin": "B001",
            "title": "USB Mouse",
            "description": [],
            "features": [],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=1, batch_size=1)

    assert results["total_documents_created"] == 1
    assert results["embedding_ready_documents"] == []
    assert results["document_quality_report"]["low_information_documents"] == 1
    assert results["document_quality_report"]["suitable_documents"] == 0


def test_pipeline_counts_metadata_preparation_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Metadata preparation failures should be counted separately."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "price": "49.99",
            "description": ["High quality wireless audio"],
            "features": ["Noise cancellation"],
        },
    ]

    def raise_metadata_error(
        product: dict[str, Any],
    ) -> dict[str, Any]:
        raise ValueError("Invalid metadata")

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )
    monkeypatch.setattr(
        product_pipeline,
        "create_product_document",
        raise_metadata_error,
    )

    results = run_product_pipeline(sample_size=1, batch_size=1)

    assert results["total_valid"] == 1
    assert results["total_documents_created"] == 0
    assert results["metadata_preparation_failures"] == 1
    assert results["embedding_ready_documents"] == []


def test_pipeline_counts_duplicate_documents_within_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count identical product documents within a batch as duplicates."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "description": ["High quality wireless audio"],
            "features": ["Bluetooth connectivity"],
        },
        {
            "parent_asin": "B002",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "description": ["High quality wireless audio"],
            "features": ["Bluetooth connectivity"],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=2, batch_size=2)

    assert results["document_quality_report"]["total_documents"] == 2
    assert results["document_quality_report"]["duplicate_documents"] == 1
    assert len(results["embedding_ready_documents"]) == 2


def test_pipeline_counts_duplicate_documents_across_batches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Identical documents in separate batches should be counted as duplicates."""

    products = [
        {
            "parent_asin": "B001",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "description": ["High quality wireless audio"],
            "features": ["Bluetooth connectivity"],
        },
        {
            "parent_asin": "B002",
            "title": "Wireless Headphones with Advanced Noise Cancellation",
            "description": ["High quality wireless audio"],
            "features": ["Bluetooth connectivity"],
        },
    ]

    monkeypatch.setattr(
        product_pipeline,
        "load_electronics_metadata",
        lambda: iter(products),
    )

    results = run_product_pipeline(sample_size=2, batch_size=1)

    assert results["document_quality_report"]["total_documents"] == 2
    assert results["document_quality_report"]["duplicate_documents"] == 1
    assert len(results["embedding_ready_documents"]) == 2
