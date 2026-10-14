from pathlib import Path

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

output_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_enriched.csv"
)


# =====================================================
# Load Silver Dataset
# =====================================================

df = pd.read_csv(silver_path)

print(f"Rows Loaded: {len(df)}")


# =====================================================
# Filter AI Articles
# Assignment Criteria:
# 1. AI_ML category
# 2. Published between 2022 and 2024
# 3. ARR > 50M USD
# =====================================================

ai_articles = df[
    (df["category_standardized"] == "AI_ML")
    & (df["year"] >= 2022)
    & (df["year"] <= 2024)
    & (df["arr_usd"] > 50_000_000)
].copy()


# =====================================================
# Select Required Columns
# =====================================================

output_columns = [
    "article_id",
    "title",
    "company_name",
    "published_date_std",
    "category_standardized",
    "arr_usd",
    "summary",
    "url",
    "industry",
    "founded_year",
    "headquarters",
    "employee_count",
    "is_public",
    "stock_ticker",
    "company_age",
    "company_size_category"
]

ai_articles = ai_articles[output_columns]


# =====================================================
# Sort Output
# =====================================================

ai_articles = ai_articles.sort_values(
    by=["published_date_std", "arr_usd"],
    ascending=[False, False]
).reset_index(drop=True)


# =====================================================
# Save File
# =====================================================

ai_articles.to_csv(
    output_path,
    index=False
)


# =====================================================
# Validation
# =====================================================

print("\n===== AI ARTICLES DATASET =====\n")

print(f"Rows Returned: {len(ai_articles)}")

print(
    ai_articles[
        [
            "article_id",
            "company_name",
            "category_standardized",
            "arr_usd"
        ]
    ].head(10)
)

print(
    f"\nSaved: {output_path}"
)