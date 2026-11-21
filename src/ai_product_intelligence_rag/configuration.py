
"""
Load and validate application configuration.
"""

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "dataset_config.yaml"


def load_dataset_config(
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> dict[str, Any]:
    """
    Load dataset configuration from a YAML file.
    """

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    if not isinstance(config, dict):
        raise ValueError("Configuration must contain a YAML mapping.")

    required_sections = (
        "dataset",
        "processing",
        "quality",
        "documents",
        "embeddings",
    )

    for section in required_sections:
        if not isinstance(config.get(section), dict):
            raise ValueError(
                f"Missing or invalid configuration section: {section}"
            )

    return config

def validate_dataset_config(config: dict[str, Any]) -> None:
    """Validate dataset configuration values."""

    processing = config["processing"]
    dataset = config["dataset"]

    if not isinstance(dataset.get("category"), str) or not dataset["category"].strip():
        raise ValueError("Dataset category must be a non-empty string.")

    for key in ("sample_size", "batch_size", "minimum_document_length"):
        value = processing.get(key)

        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(
                f"Processing setting '{key}' must be a positive integer."
            )

    if not isinstance(dataset.get("streaming"), bool):
        raise ValueError("Dataset streaming must be a boolean.")
