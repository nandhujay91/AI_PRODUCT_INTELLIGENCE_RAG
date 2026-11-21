"""
Inspect metadata preparation using real Amazon product records.
"""

from itertools import islice

from ai_product_intelligence_rag.documents.product_document import (
    create_product_document,
)
from ai_product_intelligence_rag.ingestion.amazon_dataset import (
    load_electronics_metadata,
)
from ai_product_intelligence_rag.preprocessing.cleaning import clean_product
from ai_product_intelligence_rag.preprocessing.validation import (
    validate_product,
)


def main() -> None:
    """Inspect metadata preparation on 1,000 Amazon products."""

    dataset = load_electronics_metadata()

    processed_count = 0
    rejected_count = 0
    metadata_failure_count = 0
    prepared_count = 0
    missing_price_count = 0

    for product in islice(dataset, 1000):
        errors = validate_product(product)

        if errors:
            rejected_count += 1
            continue

        cleaned_product = clean_product(product)
        processed_count += 1

        try:
            document = create_product_document(cleaned_product)
        except ValueError:
            metadata_failure_count += 1
            continue

        prepared_count += 1

        if "price" not in document["metadata"]:
            missing_price_count += 1

    print("\nAmazon Product Metadata Preparation Report")
    print("=" * 55)

    print(f"Processed products: {processed_count}")
    print(f"Rejected products: {rejected_count}")
    print(f"Metadata preparation failures: {metadata_failure_count}")
    print(f"Successfully prepared metadata: {prepared_count}")
    print(f"Products with missing prices: {missing_price_count}")


if __name__ == "__main__":
    main()
