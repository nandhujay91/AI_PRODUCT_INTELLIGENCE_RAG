"""
Inspect a small sample of Amazon Electronics products.
"""

from itertools import islice

from ai_product_intelligence_rag.ingestion.amazon_dataset import (
    load_electronics_metadata,
)

MAX_RECORDS = 3


def inspect_product(product: dict, product_number: int) -> None:
    """Display important product information and data types."""

    price = product.get("price")

    print(f"\nProduct {product_number}")
    print(f"Title: {product.get('title')}")
    print(f"Product ID: {product.get('parent_asin')}")
    print(f"Price value: {price!r}")
    print(f"Price type: {type(price).__name__}")
    print("-" * 50)


def main() -> None:
    """Connect to the dataset and inspect sample products."""

    print("Connecting to Amazon Electronics dataset...")

    dataset = load_electronics_metadata()

    print("\nConnection successful!")
    print("\nDataset columns:")

    if dataset.features:
        for column_name in dataset.features:
            print(f"- {column_name}")

    print(f"\nInspecting first {MAX_RECORDS} products...")

    for product_number, product in enumerate(
        islice(dataset, MAX_RECORDS),
        start=1,
    ):
        inspect_product(product, product_number)


if __name__ == "__main__":
    main()
