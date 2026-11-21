"""
Inspect cleaned Amazon Electronics product records.
"""

from itertools import islice
from pprint import pprint

from ai_product_intelligence_rag.ingestion.amazon_dataset import (
    load_electronics_metadata,
)
from ai_product_intelligence_rag.preprocessing.cleaning import clean_product
from ai_product_intelligence_rag.preprocessing.validation import (
    validate_product,
)


def main() -> None:
    """Load, validate and inspect a small sample of cleaned products."""

    dataset = load_electronics_metadata()

    inspected_count = 0

    for product in islice(dataset, 10):
        errors = validate_product(product)

        if errors:
            continue

        cleaned_product = clean_product(product)

        inspected_count += 1

        print(f"\nCleaned Product {inspected_count}")
        print("=" * 50)
        pprint(cleaned_product, sort_dicts=False)

        if inspected_count == 3:
            break

    print(f"\nTotal cleaned products inspected: {inspected_count}")


if __name__ == "__main__":
    main()
