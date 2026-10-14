from pathlib import Path
import duckdb
import pandas as pd


# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

silver_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "articles_enriched.csv"
)

gold_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
)

gold_path.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# Load Silver Dataset
# =====================================================

df = pd.read_csv(silver_path)

print(f"Rows Loaded: {len(df)}")


# =====================================================
# DIM COMPANY
# =====================================================

dim_company = (

    df[
        [
            "company_name",
            "industry",
            "headquarters",
            "employee_count",
            "founded_year",
            "is_public",
            "stock_ticker",
            "company_size_category"
        ]
    ]
    .drop_duplicates(subset=["company_name"])
    .reset_index(drop=True)

)

dim_company = dim_company.sort_values(
    "company_name"
).reset_index(drop=True)

dim_company.insert(
    0,
    "company_key",
    range(1, len(dim_company) + 1)
)

print(
    f"dim_company rows: {len(dim_company)}"
)


# =====================================================
# DIM ARTICLE
# =====================================================

dim_article = (

    df[
        [
            "article_id",
            "title",
            "summary",
            "url",
            "author",
            "published_date_std",
            "year",
            "month",
            "quarter",
            "category_standardized"
        ]
    ]
    .drop_duplicates(subset=["article_id"])
    .reset_index(drop=True)

)
dim_article = (
    dim_article
    .sort_values("article_id")
    .reset_index(drop=True)
)
print(
    f"dim_article rows: {len(dim_article)}"
)


# =====================================================
# FACT ARR OBSERVATION
# =====================================================

fact_arr = (

    df[
        [
            "article_id",
            "company_name",
            "published_date_std",
            "arr_usd",
            "revenue",
            "parse_status"
        ]
    ]
    .copy()

)

fact_arr = fact_arr.merge(

    dim_company[
        [
            "company_key",
            "company_name"
        ]
    ],

    on="company_name",
    how="left"
)

fact_arr.rename(

    columns={
        "published_date_std":
            "observation_date",
        "revenue":
            "raw_revenue"
    },

    inplace=True
)

fact_arr = (
    fact_arr
    .sort_values("article_id")
    .reset_index(drop=True)
)

fact_arr.insert(
    0,
    "observation_id",
    range(1, len(fact_arr) + 1)
)

fact_arr = fact_arr[
    [
        "observation_id",
        "article_id",
        "company_key",
        "observation_date",
        "arr_usd",
        "raw_revenue",
        "parse_status"
    ]
]

print(
    f"fact_arr rows: {len(fact_arr)}"
)


# =====================================================
# SAVE FILES
# =====================================================

dim_company.to_csv(
    gold_path / "dim_company.csv",
    index=False
)

dim_article.to_csv(
    gold_path / "dim_article.csv",
    index=False
)

fact_arr.to_csv(
    gold_path / "fact_arr_observation.csv",
    index=False
)

print(
    "\nWarehouse Model Created Successfully"
)

print(
    f"Saved: {gold_path}"
)
print(dim_company.head())
print(dim_article.head())
print(fact_arr.head())
print(dim_company["company_key"].nunique())
print(len(dim_company))
print(dim_article["article_id"].nunique())
print(len(dim_article))
print(fact_arr["observation_id"].nunique())
print(len(fact_arr))

# =====================================================
# CREATE DUCKDB WAREHOUSE
# =====================================================

duckdb_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "warehouse.duckdb"
)

conn = duckdb.connect(
    str(duckdb_path)
)

conn.register(
    "dim_company_df",
    dim_company
)

conn.register(
    "dim_article_df",
    dim_article
)

conn.register(
    "fact_arr_df",
    fact_arr
)

conn.execute("""
CREATE OR REPLACE TABLE dim_company AS
SELECT * FROM dim_company_df
""")

conn.execute("""
CREATE OR REPLACE TABLE dim_article AS
SELECT * FROM dim_article_df
""")

conn.execute("""
CREATE OR REPLACE TABLE fact_arr_observation AS
SELECT * FROM fact_arr_df
""")

conn.close()

print(
    f"DuckDB warehouse created: {duckdb_path}"
)