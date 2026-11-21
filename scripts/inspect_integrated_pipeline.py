"""
Inspect the integrated Amazon product processing pipeline.
"""

from ai_product_intelligence_rag.preprocessing.product_pipeline import (
    run_product_pipeline,
)


def main() -> None:
    """Run the integrated pipeline on 1,000 Amazon products."""

    results = run_product_pipeline(
        sample_size=1000,
        batch_size=100,
    )

    print("\nAmazon Product Intelligence Pipeline Report")
    print("=" * 60)

    print("\nProduct Processing")
    print("-" * 60)

    print(f"Total processed: {results['total_processed']}")
    print(f"Valid products: {results['total_valid']}")
    print(f"Rejected products: {results['total_rejected']}")

    print("\nProduct Quality")
    print("-" * 60)

    for metric, value in results["quality_report"].items():
        print(f"{metric}: {value}")

    print("\nDocument Processing")
    print("-" * 60)

    print(f"Documents created: {results['total_documents_created']}")
    print(f"Metadata preparation failures: {results['metadata_preparation_failures']}")

    print("\nDocument Quality")
    print("-" * 60)

    for metric, value in results["document_quality_report"].items():
        print(f"{metric}: {value}")

    print("\nEmbedding Readiness")
    print("-" * 60)

    print(f"Embedding-ready documents: {len(results['embedding_ready_documents'])}")


if __name__ == "__main__":
    main()
