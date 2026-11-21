
"""
Run the Amazon product processing pipeline.
"""

from ai_product_intelligence_rag.preprocessing.product_pipeline import (
    run_product_pipeline,
)


def main() -> None:
    """Execute the pipeline and display processing statistics."""

    try:
        results = run_product_pipeline(
            sample_size=1000,
            batch_size=100,
        )
    except Exception as error:
        print("\nAmazon Product Pipeline Failed")
        print("--------------------------------")
        print(f"Error: {error}")
        raise

    print("\nAmazon Product Pipeline Results")
    print("--------------------------------")
    print(f"Total processed: {results['total_processed']}")
    print(f"Valid products: {results['total_valid']}")
    print(f"Rejected products: {results['total_rejected']}")
    print(
        "Documents created: "
        f"{results['total_documents_created']}"
    )
    print(
        "Metadata preparation failures: "
        f"{results['metadata_preparation_failures']}"
    )

    print("\nProduct Data Quality Report")
    print("---------------------------")

    for metric, value in results["quality_report"].items():
        print(f"{metric}: {value}")

    print("\nDocument Quality Report")
    print("-----------------------")

    for metric, value in results["document_quality_report"].items():
        print(f"{metric}: {value}")

    print("\nEmbedding Readiness")
    print("-------------------")
    print(
        "Embedding-ready documents: "
        f"{len(results['embedding_ready_documents'])}"
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
