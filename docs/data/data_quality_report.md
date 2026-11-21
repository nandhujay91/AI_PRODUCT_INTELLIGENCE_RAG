
# Amazon Electronics — Data Quality Report

## 1. Purpose

This report documents the data-quality assessment performed on Amazon Electronics product metadata.

## 2. Initial Dataset Profiling

Sample size: 10,000 records.

| Metric | Result |
|---|---:|
| Total records | 10,000 |
| Missing product IDs | 0 |
| Missing titles | 0 |
| Missing prices | 5,718 |
| Empty descriptions | 4,238 |
| Empty features | 2,202 |
| Duplicate product IDs | 0 |
| Valid prices | 4,282 |

## 3. Price Analysis

| Metric | Value |
|---|---:|
| Minimum price | 0.93 |
| Maximum price | 12,998.00 |
| Average price | 88.71 |
| Median price | 20.39 |

The average is considerably higher than the median, indicating the influence of expensive products.

## 4. Integrated Pipeline Results

Sample size: 1,000 records.

| Metric | Result |
|---|---:|
| Total processed | 1,000 |
| Valid products | 1,000 |
| Rejected products | 0 |
| Missing product IDs | 0 |
| Missing titles | 0 |
| Missing prices | 568 |
| Missing descriptions | 444 |
| Missing features | 229 |
| Duplicate product IDs | 0 |

## 5. Document Quality Results

| Metric | Result |
|---|---:|
| Documents created | 1,000 |
| Empty documents | 0 |
| Low-information documents | 5 |
| Duplicate documents | 0 |
| Suitable documents | 995 |
| Embedding-ready documents | 995 |
| Metadata preparation failures | 0 |

## 6. Data Quality Decisions

- Missing prices are allowed.
- Missing descriptions and features are allowed.
- Product identifiers and titles are required.
- Invalid non-missing values are rejected during validation.
- Duplicate product identifiers are tracked.
- Duplicate document content is tracked using SHA-256 hashes.
- Documents shorter than 30 characters are excluded from embedding-ready output.

## 7. Conclusion

The integrated pipeline successfully processed the 1,000-record sample.

All 1,000 products passed product validation. The pipeline generated 1,000 product documents, of which 995 met the configured document-quality threshold.

These results establish the initial data-quality baseline for the next engineering phase.
