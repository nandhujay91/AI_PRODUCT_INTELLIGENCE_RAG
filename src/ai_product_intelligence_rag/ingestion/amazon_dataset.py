"""
Connect to Amazon Electronics metadata through remote Parquet files.
"""

from datasets import IterableDataset, load_dataset

REPOSITORY_URL = (
    "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/"
)

PARQUET_FILES = [
    f"{REPOSITORY_URL}raw_meta_Electronics/full-{file_number:05d}-of-00010.parquet"
    for file_number in range(10)
]


def load_electronics_metadata() -> IterableDataset:
    """Stream product metadata directly from remote Parquet files."""

    try:
        return load_dataset(
            "parquet",
            data_files=PARQUET_FILES,
            split="train",
            streaming=True,
        )

    except Exception as error:
        raise RuntimeError("Unable to stream Amazon Electronics metadata.") from error
