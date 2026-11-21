"""
Inspect the quality of documents created from Amazon products.
"""

from itertools import islice

from ai_product_intelligence_rag.documents.document_quality_report import (
    generate_document_quality_report,
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
    """Generate and inspect a quality report from real Amazon products."""

    dataset = load_electronics_metadata()

    documents = []

    processed_count = 0
    rejected_count = 0

    for product in islice(dataset, 1000):
        errors = validate_product(product)

        if errors:
            rejected_count += 1
            continue

        cleaned_product = clean_product(product)
        document = create_product_document(cleaned_product)

        documents.append(document)
        processed_count += 1

    report = generate_document_quality_report(
        documents,
        min_length=30,
    )

    print("\nAmazon Product Document Quality Report")
    print("=" * 50)

    print(f"Processed products: {processed_count}")
    print(f"Rejected products: {rejected_count}")

    print("\nDocument Quality Metrics")
    print("-" * 50)

    for metric, value in report.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
