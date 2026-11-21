"""
Create structured documents from cleaned Amazon product records.
"""

from typing import Any

from ai_product_intelligence_rag.documents.metadata_preparation import (
    prepare_chroma_metadata,
)


def create_product_document(product: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a cleaned product record into a document with metadata.

    Args:
        product: A cleaned Amazon product record.

    Returns:
        A dictionary containing document text and validated metadata.
    """

    document_sections = [
        f"Product: {product['title']}",
    ]

    description = product.get("description", [])

    if description:
        document_sections.append(f"Description: {' '.join(description)}")

    features = product.get("features", [])

    if features:
        document_sections.append(f"Features: {' '.join(features)}")

    page_content = "\n\n".join(document_sections)

    metadata = {
        "parent_asin": product["parent_asin"],
        "title": product["title"],
        "price": product.get("price"),
        "average_rating": product.get("average_rating"),
        "rating_number": product.get("rating_number"),
        "main_category": product.get("main_category"),
        "store": product.get("store"),
    }

    prepared_metadata = prepare_chroma_metadata(metadata)

    return {
        "page_content": page_content,
        "metadata": prepared_metadata,
    }
