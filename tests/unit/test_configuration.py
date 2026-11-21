
"""Unit tests for application configuration."""

import pytest

from ai_product_intelligence_rag.configuration import (
    load_dataset_config,
    validate_dataset_config,
)


def test_load_dataset_config() -> None:
    """The project YAML configuration should load successfully."""

    config = load_dataset_config()

    assert config["dataset"]["category"] == "Electronics"
    assert config["processing"]["sample_size"] == 1000
    assert config["processing"]["batch_size"] == 100
    assert config["processing"]["minimum_document_length"] == 30


def test_validate_dataset_config() -> None:
    """Valid configuration should pass validation."""

    config = load_dataset_config()

    validate_dataset_config(config)


def test_reject_invalid_sample_size() -> None:
    """A non-positive sample size should be rejected."""

    config = load_dataset_config()
    config["processing"]["sample_size"] = 0

    with pytest.raises(ValueError):
        validate_dataset_config(config)


def test_reject_invalid_batch_size() -> None:
    """A non-positive batch size should be rejected."""

    config = load_dataset_config()
    config["processing"]["batch_size"] = -1

    with pytest.raises(ValueError):
        validate_dataset_config(config)


def test_reject_invalid_minimum_document_length() -> None:
    """A non-positive document length should be rejected."""

    config = load_dataset_config()
    config["processing"]["minimum_document_length"] = 0

    with pytest.raises(ValueError):
        validate_dataset_config(config)


def test_reject_invalid_dataset_category() -> None:
    """An empty dataset category should be rejected."""

    config = load_dataset_config()
    config["dataset"]["category"] = ""

    with pytest.raises(ValueError):
        validate_dataset_config(config)


def test_reject_invalid_streaming_setting() -> None:
    """A non-boolean streaming setting should be rejected."""

    config = load_dataset_config()
    config["dataset"]["streaming"] = "true"

    with pytest.raises(ValueError):
        validate_dataset_config(config)


def test_reject_missing_configuration_file(tmp_path) -> None:
    """A missing configuration file should raise FileNotFoundError."""

    missing_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_dataset_config(missing_file)
