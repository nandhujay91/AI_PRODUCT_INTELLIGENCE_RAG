"""
Run basic profiling on Amazon Electronics metadata.
"""

from ai_product_intelligence_rag.ingestion.amazon_dataset import (
    load_electronics_metadata,
)
from ai_product_intelligence_rag.preprocessing.profile import (
    profile_products,
)

SAMPLE_SIZE = 10000


def main() -> None:
    """Load and profile a sample of Amazon products."""

    print("Connecting to Amazon Electronics dataset...")

    dataset = load_electronics_metadata()

    print(f"\nProfiling first {SAMPLE_SIZE} products...")

    metrics = profile_products(dataset, SAMPLE_SIZE)

    print("\nDATA QUALITY PROFILE")
    print("=" * 40)

    for metric, value in metrics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
