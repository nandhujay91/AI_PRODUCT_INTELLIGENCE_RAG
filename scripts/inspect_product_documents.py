"""
Inspect documents created from real Amazon Electronics products.
"""

from itertools import islice
from pprint import pprint

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
    """Create and inspect documents from real Amazon product records."""

    dataset = load_electronics_metadata()

    inspected_count = 0

    for product in islice(dataset, 20):
        errors = validate_product(product)

        if errors:
            continue

        cleaned_product = clean_product(product)
        document = create_product_document(cleaned_product)

        inspected_count += 1

        print(f"\nProduct Document {inspected_count}")
        print("=" * 60)

        print("\nDOCUMENT TEXT")
        print("-" * 60)
        print(document["page_content"])

        print("\nMETADATA")
        print("-" * 60)
        pprint(document["metadata"], sort_dicts=False)

        if inspected_count == 3:
            break

    print(f"\nTotal documents inspected: {inspected_count}")


if __name__ == "__main__":
    main()
