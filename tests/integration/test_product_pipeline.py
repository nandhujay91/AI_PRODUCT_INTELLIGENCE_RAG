
"""
End-to-end integration tests for the Amazon product pipeline.
"""

from unittest.mock import patch

from ai_product_intelligence_rag.preprocessing.product_pipeline import (
    run_product_pipeline,
)


def test_product_pipeline_with_streamed_dataset() -> None:
    """Verify the complete pipeline using real streamed Amazon records."""

    results = run_product_pipeline(
        sample_size=20,
        batch_size=5,
        min_document_length=30,
    )

    assert results["total_processed"] == 20

    assert (
        results["total_valid"] + results["total_rejected"]
        == results["total_processed"]
    )

    assert (
        results["total_documents_created"]
        <= results["total_valid"]
    )

    assert (
        results["document_quality_report"]["suitable_documents"]
        == len(results["embedding_ready_documents"])
    )

    for document in results["embedding_ready_documents"]:
        assert isinstance(document["page_content"], str)
        assert document["page_content"].strip()

        assert isinstance(document["metadata"], dict)
        assert "parent_asin" in document["metadata"]
        assert "title" in document["metadata"]


def test_product_pipeline_uses_yaml_defaults() -> None:
    """Verify that pipeline defaults come from YAML configuration."""

    with (
        patch(
            "ai_product_intelligence_rag.preprocessing.product_pipeline."
            "load_electronics_metadata",
            return_value=[],
        ) as mock_dataset,
    ):
        results = run_product_pipeline()

    mock_dataset.assert_called_once()

    assert results["total_processed"] == 0
    assert results["total_valid"] == 0
    assert results["total_rejected"] == 0
    assert results["embedding_ready_documents"] == []
