
"""
Prepare Amazon product records for downstream processing.
"""

import hashlib
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import Any

from ai_product_intelligence_rag.configuration import (
    load_dataset_config,
    validate_dataset_config,
)
from ai_product_intelligence_rag.documents.document_quality import (
    is_document_empty,
    is_document_low_information,
)
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
from ai_product_intelligence_rag.preprocessing.quality_report import (
    generate_quality_report,
)
from ai_product_intelligence_rag.preprocessing.validation import (
    validate_product,
)


def process_product_batch(
    products: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Validate and clean a batch of Amazon products."""

    valid_products = []
    rejected_products = []

    for product in products:
        errors = validate_product(product)

        if errors:
            rejected_products.append(
                {
                    "product": product,
                    "errors": errors,
                }
            )
        else:
            valid_products.append(clean_product(product))

    return {
        "valid_products": valid_products,
        "rejected_products": rejected_products,
    }


def stream_product_batches(
    products: Iterable[dict[str, Any]],
    batch_size: int,
) -> Iterator[list[dict[str, Any]]]:
    """Yield product records in batches without loading the entire dataset."""

    if (
        isinstance(batch_size, bool)
        or not isinstance(batch_size, int)
        or batch_size <= 0
    ):
        raise ValueError("Batch size must be a positive integer.")

    product_iterator = iter(products)

    while batch := list(islice(product_iterator, batch_size)):
        yield batch


def run_product_pipeline(
    sample_size: int | None = None,
    batch_size: int | None = None,
    min_document_length: int | None = None,
) -> dict[str, Any]:
    """
    Stream, validate, clean and prepare Amazon product documents.

    Processing defaults are loaded from the YAML configuration.
    Explicit function arguments override configured values.

    Product and document duplicate counts include duplicates within
    and across batches.

    Only documents suitable for embedding are retained in the output.
    """

    # Load and validate project configuration.
    config = load_dataset_config()
    validate_dataset_config(config)

    processing_config = config["processing"]

    # Use explicit arguments when supplied; otherwise use YAML values.
    sample_size = (
        processing_config["sample_size"]
        if sample_size is None
        else sample_size
    )

    batch_size = (
        processing_config["batch_size"]
        if batch_size is None
        else batch_size
    )

    min_document_length = (
        processing_config["minimum_document_length"]
        if min_document_length is None
        else min_document_length
    )

    # Validate resolved processing parameters.
    processing_parameters = {
        "sample_size": sample_size,
        "batch_size": batch_size,
        "minimum_document_length": min_document_length,
    }

    for parameter, value in processing_parameters.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value <= 0
        ):
            raise ValueError(
                f"Processing parameter '{parameter}' "
                "must be a positive integer."
            )

    dataset = load_electronics_metadata()

    total_valid = 0
    total_rejected = 0
    total_processed = 0
    total_documents_created = 0
    metadata_preparation_failures = 0

    quality_report = {
        "total_records": 0,
        "missing_product_ids": 0,
        "missing_titles": 0,
        "missing_prices": 0,
        "missing_descriptions": 0,
        "missing_features": 0,
        "duplicate_product_ids": 0,
    }

    seen_product_ids = set()
    cross_batch_product_duplicates = 0

    seen_document_hashes = set()
    cross_batch_document_duplicates = 0

    embedding_ready_documents = []

    document_quality_totals = {
        "total_documents": 0,
        "empty_documents": 0,
        "low_information_documents": 0,
        "duplicate_documents": 0,
        "suitable_documents": 0,
    }

    sampled_products = islice(dataset, sample_size)

    for batch in stream_product_batches(sampled_products, batch_size):
        results = process_product_batch(batch)

        valid_products = results["valid_products"]

        total_valid += len(valid_products)
        total_rejected += len(results["rejected_products"])
        total_processed += len(batch)

        # Generate product-level quality metrics.
        batch_quality_report = generate_quality_report(batch)

        for metric, value in batch_quality_report.items():
            quality_report[metric] += value

        # Detect product duplicates across batches.
        batch_product_ids = set()

        for product in batch:
            product_id = product.get("parent_asin")

            if not isinstance(product_id, str) or not product_id.strip():
                continue

            normalized_id = product_id.strip()

            if normalized_id in batch_product_ids:
                continue

            batch_product_ids.add(normalized_id)

            if normalized_id in seen_product_ids:
                cross_batch_product_duplicates += 1

        seen_product_ids.update(batch_product_ids)

        # Generate documents and prepare metadata.
        batch_documents = []

        for product in valid_products:
            try:
                document = create_product_document(product)
            except ValueError:
                metadata_preparation_failures += 1
                continue

            batch_documents.append(document)
            total_documents_created += 1

        # Calculate document-quality metrics for this batch.
        batch_document_report = generate_document_quality_report(
            batch_documents,
            min_length=min_document_length,
        )

        for metric in document_quality_totals:
            document_quality_totals[metric] += batch_document_report[metric]

        # Detect duplicate document contents using SHA-256 hashes.
        batch_document_hashes = set()

        for document in batch_documents:
            page_content = document.get("page_content")

            if is_document_empty(page_content):
                continue

            normalized_content = page_content.strip()

            content_hash = hashlib.sha256(
                normalized_content.encode("utf-8")
            ).hexdigest()

            # Batch-level duplicates are already counted by the
            # document-quality report.
            if content_hash in batch_document_hashes:
                continue

            batch_document_hashes.add(content_hash)

            # Count duplicates found in previous batches.
            if content_hash in seen_document_hashes:
                cross_batch_document_duplicates += 1

        seen_document_hashes.update(batch_document_hashes)

        # Retain documents suitable for embedding.
        for document in batch_documents:
            page_content = document.get("page_content")

            if is_document_empty(page_content):
                continue

            if is_document_low_information(
                page_content,
                min_length=min_document_length,
            ):
                continue

            embedding_ready_documents.append(document)

    # Add cross-batch product duplicates.
    quality_report["duplicate_product_ids"] += cross_batch_product_duplicates

    # Add cross-batch document duplicates.
    document_quality_totals["duplicate_documents"] += (
        cross_batch_document_duplicates
    )

    return {
        "total_processed": total_processed,
        "total_valid": total_valid,
        "total_rejected": total_rejected,
        "quality_report": quality_report,
        "total_documents_created": total_documents_created,
        "embedding_ready_documents": embedding_ready_documents,
        "document_quality_report": document_quality_totals,
        "metadata_preparation_failures": metadata_preparation_failures,
    }
