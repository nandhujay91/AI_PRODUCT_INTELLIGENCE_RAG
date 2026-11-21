"""
Integration tests for Amazon Electronics dataset ingestion.
"""

from itertools import islice

from ai_product_intelligence_rag.ingestion.amazon_dataset import (
    load_electronics_metadata,
)
from ai_product_intelligence_rag.preprocessing.validation import (
    validate_product,
)


def test_amazon_dataset_streaming() -> None:
    """Verify that Amazon product records can be streamed."""

    dataset = load_electronics_metadata()

    products = list(islice(dataset, 5))

    assert len(products) == 5

    for product in products:
        assert isinstance(product, dict)
        assert "parent_asin" in product
        assert "title" in product


def test_amazon_products_pass_validation() -> None:
    """Validate a sample of streamed Amazon products."""

    dataset = load_electronics_metadata()

    products = list(islice(dataset, 5))

    for product in products:
        errors = validate_product(product)

        assert errors == [], (
            f"Product {product.get('parent_asin')} failed validation: {errors}"
        )
