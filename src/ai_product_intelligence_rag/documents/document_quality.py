
"""
Validate the quality of product documents before embedding.
"""

import hashlib
from collections.abc import Iterable
from typing import Any


def is_document_empty(page_content: object) -> bool:
    """
    Check whether document content is missing or contains only whitespace.
    """

    return not isinstance(page_content, str) or not page_content.strip()


MIN_DOCUMENT_LENGTH = 30


def is_document_low_information(
    page_content: object,
    min_length: int = MIN_DOCUMENT_LENGTH,
) -> bool:
    """
    Check whether a document contains too little text.

    The document is considered low-information when its stripped
    content is shorter than the configured minimum length.
    """

    if min_length <= 0:
        raise ValueError("Minimum document length must be greater than zero.")

    if is_document_empty(page_content):
        return True

    return len(page_content.strip()) < min_length


def count_duplicate_documents(
    documents: Iterable[dict[str, Any]],
) -> int:
    """
    Count repeated document contents using SHA-256 hashes.

    Each repeated occurrence after the first is counted as a duplicate.
    Surrounding whitespace is ignored.
    """

    seen_hashes = set()
    duplicate_count = 0

    for document in documents:
        page_content = document.get("page_content")

        if is_document_empty(page_content):
            continue

        normalized_content = page_content.strip()
        content_hash = hashlib.sha256(
            normalized_content.encode("utf-8")
        ).hexdigest()

        if content_hash in seen_hashes:
            duplicate_count += 1
        else:
            seen_hashes.add(content_hash)

    return duplicate_count
