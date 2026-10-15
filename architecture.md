# Data Architecture

## Overview

This solution follows a Bronze → Silver → Gold architecture.

The objective is to transform raw article data into a warehouse-ready ARR observation model that supports:

- ARR trend analysis
- Source lineage tracking
- AI article discovery
- Semantic search
- Similarity-based recommendations

---

# Bronze Layer

Raw source files.

Inputs:

```text
tech_news.csv
company_metadata.json
```

Characteristics:

- immutable source data
- no transformations applied
- serves as system of record

---

# Silver Layer

Intermediate cleaned and enriched datasets.

Output:

```text
articles_enriched.csv
```

Transformations:

### Revenue

- ARR normalization
- Currency conversion
- Range midpoint calculation
- Missing value handling

### Dates

- ISO parsing
- US parsing
- EU parsing
- Datetime normalization

Generated fields:

```text
year
month
quarter
```

### Categories

Mapped to taxonomy:

```text
AI_ML
CLOUD
FINTECH
DATA_ANALYTICS
SOFTWARE
CYBERSECURITY
```

### Company Enrichment

Additional metadata:

```text
industry
founded_year
headquarters
employee_count
is_public
stock_ticker
company_age
company_size_category
```

---

# Gold Layer

Warehouse-ready analytical model.

---

## dim_company

Grain:

```text
One row per company
```

Primary Key:

```text
company_key
```

Attributes:

```text
company_name
industry
headquarters
employee_count
founded_year
is_public
stock_ticker
company_size_category
```

---

## dim_article

Grain:

```text
One row per article
```

Primary Key:

```text
article_id
```

Attributes:

```text
title
summary
url
author
published_date
year
month
quarter
category
```

---

## fact_arr_observation

Grain:

```text
One ARR observation extracted from one article
```

Primary Key:

```text
observation_id
```

Foreign Keys:

```text
company_key -> dim_company
article_id -> dim_article
```

Measures:

```text
arr_usd
```

Additional attributes:

```text
raw_revenue
parse_status
observation_date
```

---

# Relationship Model

```text
dim_company
      |
      | company_key
      |
fact_arr_observation
      |
      | article_id
      |
dim_article
```

---

# Data Lineage

ARR observations retain complete traceability.

Lineage path:

```text
ARR Observation
        ↓
fact_arr_observation
        ↓
article_id
        ↓
dim_article
        ↓
title
summary
url
```

This allows any modeled ARR observation to be traced back to its original source article.

---

# Invalid ARR Handling

Invalid or undisclosed ARR observations are preserved.

Examples:

```text
N/A
Not disclosed
Null
```

Stored as:

```text
arr_usd = NULL
parse_status = MISSING
```

This preserves lineage while avoiding false ARR observations.

---

# ARR Querying

## ARR History

Supported through:

```text
fact_arr_observation
```

Example:

```text
Company
Date
ARR
```

over time.

---

## Latest ARR

Derived using:

```sql
ROW_NUMBER()
OVER (
PARTITION BY company_key
ORDER BY observation_date DESC
)
```

---

## Quarterly ARR

Derived using:

```text
fact_arr_observation
+
year
+
quarter
```

from article dimension.

---

# Semantic Search Architecture

Input text:

```text
title + summary
```

Embedding model:

```text
SentenceTransformer
all-MiniLM-L6-v2
```

Process:

```text
Article
    ↓
Embedding
    ↓
Cosine Similarity
    ↓
Similar Articles
```

Outputs:

```text
embedding
top_similar_articles
```

---

# Hybrid Search

Hybrid search combines:

Business filters:

```text
AI category OR AI industry
2022-2024
ARR > 50M
```

with:

```text
Semantic similarity search
```

This enables retrieval of AI-related ARR observations that are semantically similar to a user query.

---

# DuckDB

The warehouse is additionally materialized as:

```text
warehouse.duckdb
```

Benefits:

- local SQL analytics
- rapid filtering
- easy ARR trend analysis
- reproducible warehouse model

---

# Reliability Beyond Local Batch

For production deployment:

## Orchestration

Use:

```text
Airflow
Azure Data Factory
GitHub Actions
```

## Incremental Processing

Use:

```text
article_id
```

as the natural business key.

Implement:

```text
MERGE
UPSERT
```

for new article arrivals.

## Monitoring

Track:

```text
failed parses
unmatched companies
missing ARR values
```

## Data Quality

Validate:

```text
revenue formats
date formats
company mappings
```

on every ingestion run.

---

# Idempotency

The current implementation uses a full-refresh pattern.

Running the pipeline multiple times produces the same warehouse outputs because:

```text
duplicate records are removed
business keys are preserved
outputs are deterministically rebuilt
```

This satisfies the assignment requirement for duplicate-free reruns.