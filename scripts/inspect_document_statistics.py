"""
Inspect text-length statistics for real Amazon product documents.
"""

from itertools import islice

from ai_product_intelligence_rag.documents.document_statistics import (
    calculate_document_statistics,
)
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
    """Calculate document length statistics for 1,000 products."""

    dataset = load_electronics_metadata()

    documents = []
    rejected_count = 0

    for product in islice(dataset, 1000):
        errors = validate_product(product)

        if errors:
            rejected_count += 1
            continue

        cleaned_product = clean_product(product)
        document = create_product_document(cleaned_product)
        documents.append(document)

    statistics = calculate_document_statistics(documents)

    print("\nAmazon Product Document Length Statistics")
    print("=" * 55)

    print(f"Rejected products: {rejected_count}")

    for metric, value in statistics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
