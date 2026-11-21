"""
Unit tests for Amazon product document creation.
"""

from ai_product_intelligence_rag.documents.product_document import (
    create_product_document,
)


def test_create_product_document() -> None:
    """A complete product should produce document text and metadata."""

    product = {
        "parent_asin": "B001",
        "title": "Wireless Headphones",
        "price": 49.99,
        "description": ["Good sound quality"],
        "features": ["Noise cancellation"],
        "average_rating": 4.5,
        "rating_number": 100,
        "main_category": "Electronics",
        "store": "Example Store",
    }

    document = create_product_document(product)

    assert "Product: Wireless Headphones" in document["page_content"]
    assert "Description: Good sound quality" in document["page_content"]
    assert "Features: Noise cancellation" in document["page_content"]

    assert document["metadata"]["parent_asin"] == "B001"
    assert document["metadata"]["price"] == 49.99


def test_create_product_document_without_description() -> None:
    """A product without a description should use its available features."""

    product = {
        "parent_asin": "B002",
        "title": "USB Keyboard",
        "price": None,
        "description": [],
        "features": ["Wireless connectivity"],
    }

    document = create_product_document(product)

    assert "Product: USB Keyboard" in document["page_content"]
    assert "Wireless connectivity" in document["page_content"]
    assert "Description:" not in document["page_content"]
    assert "price" not in document["metadata"]


def test_create_product_document_without_optional_text() -> None:
    """A product without description or features should retain its title."""

    product = {
        "parent_asin": "B003",
        "title": "USB Mouse",
        "description": [],
        "features": [],
    }

    document = create_product_document(product)

    assert document["page_content"] == "Product: USB Mouse"
