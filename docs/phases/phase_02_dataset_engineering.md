
# Phase 02 — Dataset Engineering

## 1. Objective

Build a reliable data engineering pipeline that transforms raw Amazon Electronics product metadata into validated, cleaned and structured product documents suitable for downstream embedding and retrieval.

## 2. Dataset

- Dataset: Amazon Reviews 2023
- Repository: McAuley-Lab/Amazon-Reviews-2023
- Category: Electronics
- Format: Parquet
- Ingestion: Hugging Face streaming
- Initial processing sample: 1,000 records
- Batch size: 100

## 3. Implementation Components

### 3.1 Data ingestion

Module: `ingestion/amazon_dataset.py`

- Remote Parquet ingestion.
- Streaming dataset access.
- Incremental record processing.

### 3.2 Data profiling

Module: `preprocessing/profile.py`

- Missing-value analysis.
- Product identifier analysis.
- Price statistics.
- Dataset inspection.

### 3.3 Data validation

Module: `preprocessing/validation.py`

- Required field validation.
- Price validation.
- Rating validation.
- Rating count validation.

### 3.4 Data cleaning

Module: `preprocessing/cleaning.py`

- Product identifier normalization.
- Title cleaning.
- Price conversion.
- Description and feature cleaning.
- Preservation of raw records.

### 3.5 Document engineering

Module: `documents/product_document.py`

- Product document generation.
- Page-content construction.
- Structured metadata generation.

### 3.6 Metadata engineering

Modules:
- `documents/metadata_validation.py`
- `documents/metadata_preparation.py`

- Required metadata validation.
- Supported type validation.
- Missing optional metadata handling.
- Non-finite numeric value rejection.

### 3.7 Document quality

Modules:
- `documents/document_quality.py`
- `documents/document_quality_report.py`
- `documents/document_statistics.py`

- Empty-document detection.
- Minimum-length validation.
- Duplicate detection.
- Document statistics.
- Embedding-ready document selection.

### 3.8 Integrated pipeline

Module: `preprocessing/product_pipeline.py`

- Batch processing.
- Product validation and cleaning.
- Product document generation.
- Metadata preparation.
- Quality reporting.
- Duplicate tracking within and across batches.
- Embedding-ready document selection.

## 4. Engineering Decisions

| Decision | Reason |
|---|---|
| Streaming ingestion | Avoid loading the complete source dataset |
| Batch processing | Control processing memory |
| Missing prices allowed | Preserve valid products with incomplete optional data |
| Raw records preserved | Avoid modifying source data |
| Structured metadata | Support vector database filtering |
| SHA-256 duplicate tracking | Reduce memory used for document duplicate tracking |
| Minimum document length of 30 | Exclude very short documents |
| Product-level documents | Preserve product information as a single retrieval unit initially |

## 5. Actual Pipeline Results

Integrated run using 1,000 records:

| Metric | Result |
|---|---:|
| Processed products | 1,000 |
| Valid products | 1,000 |
| Rejected products | 0 |
| Missing prices | 568 |
| Missing descriptions | 444 |
| Missing features | 229 |
| Duplicate product IDs | 0 |
| Documents created | 1,000 |
| Metadata preparation failures | 0 |
| Empty documents | 0 |
| Low-information documents | 5 |
| Duplicate documents | 0 |
| Suitable documents | 995 |
| Embedding-ready documents | 995 |

## 6. Testing

Unit tests cover:

- Dataset validation.
- Product cleaning.
- Product quality reporting.
- Document generation.
- Metadata validation.
- Metadata preparation.
- Document quality.
- Document statistics.
- Integrated product pipeline.

Integration tests cover Amazon dataset ingestion.

## 7. Outstanding Work

- Pin an immutable dataset revision.
- Integrate YAML configuration into the application.
- Add an end-to-end data engineering integration test.
- Review production-scale document persistence.
- Perform final full-suite verification.
- Record the final pipeline execution results.

## 8. Phase Completion Criteria

Phase 02 can be signed off after:

- [x] Dataset ingestion implemented.
- [x] Streaming ingestion implemented.
- [x] Dataset profiling completed.
- [x] Product validation implemented.
- [x] Product cleaning implemented.
- [x] Product document generation implemented.
- [x] Metadata validation implemented.
- [x] Metadata preparation implemented.
- [x] Document quality checks implemented.
- [x] Integrated pipeline implemented.
- [ ] Configuration loading integrated.
- [ ] End-to-end integration testing completed.
- [ ] Final verification completed.

## 9. Current Status

Dataset engineering implementation is substantially complete.

Embedding generation and vector database ingestion have not started.

Phase 03 will begin only after Phase 02 acceptance.
