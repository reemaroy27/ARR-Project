# YipitData Data Engineering Assignment

## Overview

This project processes technology news articles and company metadata to create a warehouse-ready ARR observation model.

The pipeline performs:

- Revenue / ARR normalization
- Currency conversion
- Date standardization
- Category standardization
- Company metadata enrichment
- ARR warehouse modeling
- AI article dataset generation
- Semantic search using sentence-transformers
- Similar article recommendations
- DuckDB warehouse generation

---

# Project Structure

```text
data/
│
├── raw/
│   ├── tech_news.csv
│   └── company_metadata.json
│
├── silver/
│   ├── articles_cleaned.csv
│   └── articles_enriched.csv
│
└── gold/
    ├── dim_company.csv
    ├── dim_article.csv
    ├── fact_arr_observation.csv
    ├── ai_articles_enriched.csv
    ├── ai_articles_with_embeddings.csv
    ├── ai_articles_with_neighbors.csv
    ├── unmatched_companies.csv
    └── warehouse.duckdb

src/
│
├── main.py
├── build_warehouse.py
├── build_ai_articles.py
├── verify_duckdb.py
│
├── transformations/
│
├── embeddings/
│
└── test/
```

---

# System Requirements

- Python 3.11+
- Windows, Linux or macOS

---

# Installation

Install required packages:

```bash
pip install -r requirements.txt
```

---

# Run Pipeline

Generate cleaned and enriched datasets:

```bash
python src/main.py
```

Output:

```text
data/silver/articles_enriched.csv
```

---

# Build Warehouse

Generate warehouse tables:

```bash
python src/build_warehouse.py
```

Outputs:

```text
data/gold/dim_company.csv
data/gold/dim_article.csv
data/gold/fact_arr_observation.csv
data/gold/warehouse.duckdb
```

---

# Build AI Dataset

Generate AI-focused article dataset:

```bash
python src/build_ai_articles.py
```

Output:

```text
data/gold/ai_articles_enriched.csv
```

Selection criteria:

- category = AI_ML OR company industry = AI/ML
- published between 2022 and 2024
- ARR > 50M USD

---

# Generate Embeddings

Generate semantic embeddings:

```bash
python src/embeddings/generate_embeddings.py
```

Outputs:

```text
data/gold/ai_articles_with_embeddings.csv
data/gold/ai_articles_enriched.csv
```

Embeddings generated using:

```text
SentenceTransformer
all-MiniLM-L6-v2
```

---

# Semantic Search

Run:

```bash
python src/embeddings/similarity_search.py
```

Example:

```python
find_similar_articles(
    "large language model funding",
    top_k=5
)
```

Returns:

```text
article_id
title
company_name
similarity_score
```

---

# Hybrid Search

Run:

```bash
python src/embeddings/hybrid_search.py
```

Example:

```python
find_hybrid_articles(
    "large language model funding",
    top_k=5
)
```

Hybrid search combines:

- business filters
- semantic similarity search

Filters:

- AI category OR AI industry
- 2022-2024
- ARR > 50M USD

---

# Similar Article Recommendations

Generate nearest neighbors:

```bash
python src/embeddings/build_neighbors.py
```

Output:

```text
top_similar_articles
```

Example:

```text
ART0012|ART0045|ART0178
```

Represents the top 3 semantically similar articles.

---

# DuckDB Warehouse

Verify warehouse:

```bash
python src/verify_duckdb.py
```

The warehouse contains:

```text
dim_company
dim_article
fact_arr_observation
```

and supports SQL-based analysis.

---

# Example Queries

## ARR History

```sql
SELECT
    dc.company_name,
    f.observation_date,
    f.arr_usd
FROM fact_arr_observation f
JOIN dim_company dc
    ON f.company_key = dc.company_key
WHERE dc.company_name = 'OpenAI'
ORDER BY f.observation_date;
```

## Latest ARR Observation

```sql
SELECT *
FROM (
    SELECT
        company_key,
        observation_date,
        arr_usd,
        ROW_NUMBER() OVER (
            PARTITION BY company_key
            ORDER BY observation_date DESC
        ) rn
    FROM fact_arr_observation
)
WHERE rn = 1;
```

## Source Article Lookup

```sql
SELECT
    f.observation_id,
    a.title,
    a.url
FROM fact_arr_observation f
JOIN dim_article a
    ON f.article_id = a.article_id;
```

---

# Assumptions

## Revenue

Revenue ranges use midpoint.

Example:

```text
$10M - $20M
```

becomes:

```text
$15M
```

Currency conversion rates:

```text
EUR = USD * 1.1
GBP = USD * 1.27
JPY = USD / 150
```

## Dates

Slash-separated dates are interpreted as:

```text
MM/DD/YYYY
```

This assumption is based on values such as:

```text
02/23/2023
```

where the second value exceeds 12.

## Missing ARR Values

Records with:

```text
N/A
Not disclosed
Null
```

are retained for lineage purposes.

Stored as:

```text
arr_usd = NULL
parse_status = MISSING
```

No synthetic ARR values are generated.

## Unmatched Companies

Companies that cannot be matched to metadata are:

- logged
- flagged
- exported

Output:

```text
data/gold/unmatched_companies.csv
```
``