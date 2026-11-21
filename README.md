# AI Product Intelligence & Shopping Assistant

An AI-powered product intelligence platform using Retrieval-Augmented Generation (RAG) to help users discover, understand and compare products using evidence from a real product catalogue.

## 1. Project Overview

The platform is designed to retrieve relevant Amazon product information and generate grounded answers and product recommendations using a Large Language Model (LLM).

The project follows a production-oriented engineering approach, with emphasis on data quality, reliable ingestion, document engineering, retrieval evaluation and scalable application architecture.

## 2. Business Problem

Customers often struggle to:
- Find products that match their requirements.
- Understand product specifications.
- Compare alternative products.
- Interpret product information from large catalogues.
- Make informed purchasing decisions.

Traditional keyword-based search may not fully capture customer intent.

This platform aims to improve product discovery through semantic retrieval and evidence-based AI responses.

## 3. Project Objectives

- Build a semantic product search system.
- Implement an end-to-end RAG pipeline.
- Retrieve relevant product information.
- Generate grounded answers using an LLM.
- Compare products based on customer requirements.
- Evaluate retrieval quality and answer accuracy.
- Develop a production-oriented application.

## 4. Dataset

- **Source:** Amazon Reviews 2023
- **Repository:** McAuley-Lab/Amazon-Reviews-2023
- **Category:** Electronics
- **Access method:** Hugging Face Parquet streaming

Product metadata includes:
- Product title and description.
- Product features.
- Price and average rating.
- Rating count.
- Product category and store.
- Product identifier.

Dataset ingestion uses streaming to avoid loading the entire catalogue into memory.

## 5. Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Environment and dependency management | uv |
| Data processing | Pandas, NumPy |
| Dataset ingestion | Hugging Face Datasets |
| Configuration | YAML, PyYAML |
| Data validation and testing | Pytest |
| Code quality | Ruff |
| Document engineering | Python |
| Embeddings | Sentence Transformers (planned) |
| Vector database | ChromaDB (planned) |
| RAG orchestration | LangChain (planned) |
| API | FastAPI (planned) |
| Database | PostgreSQL (planned) |
| Monitoring | Grafana (planned) |
| Deployment | Docker (planned) |

## 6. Project Architecture

The planned application architecture consists of:

1. Dataset ingestion
2. Data validation and preprocessing
3. Product document engineering
4. Embedding generation
5. Vector database
6. Semantic retrieval
7. RAG pipeline
8. LLM integration
9. Retrieval and answer evaluation
10. API development
11. Monitoring and deployment

## 7. Development Progress

### Phase 1 — Project Setup and Architecture

- Project structure established.
- Python environment and dependency management configured.
- Initial architecture and development approach defined.

### Phase 2 — Dataset Engineering

**Status: Implementation and initial end-to-end validation completed.**

Implemented:
- Amazon Electronics metadata streaming.
- Product dataset profiling.
- Product validation and cleaning.
- Missing-value analysis.
- Product-level quality reporting.
- Product document generation.
- Metadata validation and ChromaDB-compatible preparation.
- Empty, low-information and duplicate document detection.
- Document statistics.
- YAML-based processing configuration.
- Unit and integration tests.
- End-to-end product processing pipeline.

Initial pipeline results using a 1,000-product sample:

| Metric | Result |
|---|---:|
| Products processed | 1,000 |
| Valid products | 1,000 |
| Rejected products | 0 |
| Documents created | 1,000 |
| Metadata preparation failures | 0 |
| Empty documents | 0 |
| Low-information documents | 5 |
| Duplicate documents | 0 |
| Embedding-ready documents | 995 |

These results describe the tested sample, not the entire Amazon catalogue.

### Upcoming Phases

- Phase 3 — Embedding Engineering
- Phase 4 — Vector Database and Indexing
- Phase 5 — Semantic Retrieval
- Phase 6 — RAG and LLM Integration
- Phase 7 — Evaluation and Quality Assurance
- Phase 8 — API Development
- Phase 9 — Production Deployment and Monitoring

## 8. Testing

The project uses:
- Pytest for unit and integration testing.
- Ruff for linting and code-quality checks.
- Real dataset samples for ingestion and pipeline integration tests.

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Run the product pipeline:

```bash
uv run python scripts/run_product_pipeline.py
```

## 9. Development Approach

The platform is developed incrementally.

Each phase focuses on:
- Clear engineering objectives.
- Modular implementation.
- Testable components.
- Data quality and reliability.
- Documented technical decisions.
- Integration before moving to the next phase.

The goal is to build a practical, production-oriented AI product intelligence system rather than a demonstration-only RAG application.
