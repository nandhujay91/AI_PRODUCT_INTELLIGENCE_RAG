"""
Prepare validated product metadata for ChromaDB storage.
"""

import math
from typing import Any

from ai_product_intelligence_rag.documents.metadata_validation import (
    validate_metadata,
)

SUPPORTED_METADATA_TYPES = (str, int, float, bool)


def prepare_chroma_metadata(
    metadata: dict[str, Any],
) -> dict[str, str | int | float | bool]:
    """
    Validate and prepare product metadata for ChromaDB.

    Missing optional values are omitted.

    Returns:
        A dictionary containing ChromaDB-compatible metadata.

    Raises:
        ValueError: If metadata contains invalid values or types.
    """

    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary.")

    errors = validate_metadata(metadata)

    if errors:
        raise ValueError(f"Invalid product metadata: {'; '.join(errors)}")

    prepared_metadata: dict[str, str | int | float | bool] = {}

    for key, value in metadata.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metadata keys must be non-empty strings.")

        if value is None:
            continue

        if isinstance(value, bool):
            prepared_metadata[key] = value
            continue

        if not isinstance(value, SUPPORTED_METADATA_TYPES):
            raise ValueError(f"Unsupported metadata type for field '{key}'.")

        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"Metadata field '{key}' must contain a finite number.")

        prepared_metadata[key] = value

    return prepared_metadata
