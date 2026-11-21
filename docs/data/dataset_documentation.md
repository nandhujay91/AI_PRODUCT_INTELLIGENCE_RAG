
# Amazon Electronics Dataset Documentation

## 1. Dataset Overview

| Property | Description |
|---|---|
| Dataset name | Amazon Reviews 2023 |
| Repository | McAuley-Lab/Amazon-Reviews-2023 |
| Platform | Hugging Face |
| Selected category | Electronics |
| Data format | Parquet |
| Ingestion method | Streaming |
| Processing approach | Batch processing |

## 2. Dataset Source

Hugging Face repository:

https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023

The project uses the Electronics product metadata files:

`raw_meta_Electronics/full-00000-of-00010.parquet`

The ingestion module accesses the ten Parquet shards remotely.

No manual dataset download is required.

Implementation:

`src/ai_product_intelligence_rag/ingestion/amazon_dataset.py`

## 3. Source Data Fields

The metadata contains the following fields:

| Field | Description |
|---|---|
| main_category | Product category |
| title | Product title |
| average_rating | Average customer rating |
| rating_number | Number of ratings |
| features | Product features |
| description | Product description |
| price | Product price |
| images | Product images |
| videos | Product videos |
| store | Product store |
| categories | Product category hierarchy |
| details | Additional product details |
| parent_asin | Product identifier |
| bought_together | Related products |
| subtitle | Product subtitle |
| author | Product author or creator information |

## 4. Ingestion Strategy

The dataset is accessed through Hugging Face Datasets.

The ingestion process:

1. Defines the remote Parquet shard locations.
2. Loads the dataset in streaming mode.
3. Reads records incrementally.
4. Passes records to the preprocessing pipeline.
5. Processes records in configurable batches.

This avoids downloading the entire dataset into local memory before processing.

## 5. Data Quality Considerations

The source dataset contains incomplete product information.

Important observations:

- Product prices may be missing.
- Product descriptions may be empty.
- Product features may be empty.
- Product identifiers and titles are required for valid product records.
- Optional fields should not cause otherwise valid products to be rejected.

Missing prices are retained as missing values rather than automatically replacing them with zero.

## 6. Processing Configuration

Initial pipeline configuration:

| Parameter | Value |
|---|---:|
| Sample size | 1,000 |
| Batch size | 100 |
| Minimum document length | 30 characters |
| Streaming | Enabled |
| Selected category | Electronics |

## 7. Dataset Profiling Results

Initial profiling of 10,000 records:

| Metric | Result |
|---|---:|
| Total records | 10,000 |
| Missing titles | 0 |
| Missing prices | 5,718 |
| Missing product IDs | 0 |
| Empty descriptions | 4,238 |
| Empty features | 2,202 |
| Duplicate product IDs | 0 |
| Valid prices | 4,282 |

Price statistics:

| Metric | Value |
|---|---:|
| Minimum | 0.93 |
| Maximum | 12,998.00 |
| Average | 88.71 |
| Median | 20.39 |

The average price is higher than the median, indicating that expensive products influence the price distribution.

## 8. Data Engineering Decisions

1. Retain products with missing prices.
2. Reject products without valid required identifiers or titles.
3. Validate non-missing prices.
4. Validate customer ratings and rating counts.
5. Normalize product titles and descriptions.
6. Track duplicate product identifiers.
7. Generate structured product documents for downstream retrieval.

## 9. Reproducibility

The dataset is accessed from a remote repository.

The current implementation does not pin a specific repository revision or immutable dataset snapshot.

For strict reproducibility, a dataset revision should be recorded in a future update.

The sample size and batch size are configurable through the project pipeline configuration.

## 10. Current Implementation Status

- [x] Remote dataset ingestion
- [x] Streaming support
- [x] Electronics category selection
- [x] Dataset profiling
- [x] Data validation
- [x] Data cleaning
- [x] Batch processing
- [ ] Dataset revision pinning
- [ ] Automated configuration loading
