from pathlib import Path
import json

import pandas as pd

from transformations.revenue_parser import parse_revenue
from transformations.date_parser import parse_date
from transformations.category_standardizer import standardize_category
from transformations.company_matcher import normalize_company_name
from transformations.company_enricher import get_company_size


# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

csv_path = PROJECT_ROOT / "data" / "raw" / "tech_news.csv"

json_path = PROJECT_ROOT / "data" / "raw" / "company_metadata.json"

silver_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "articles_enriched.csv"
)


# =====================================================
# Load Data
# =====================================================

print("\n===== LOADING DATA =====\n")

df = pd.read_csv(csv_path)

print(f"Articles Loaded: {len(df)}")


# =====================================================
# Revenue Parsing
# =====================================================

print("\n===== REVENUE PARSING =====\n")

df["arr_usd"] = df["revenue"].apply(parse_revenue)

df["parse_status"] = df["arr_usd"].apply(
    lambda x: "SUCCESS" if pd.notna(x) else "MISSING"
)

print("Revenue Parsing Complete")

print(
    f"Parsed Revenue Rows: "
    f"{df['arr_usd'].notna().sum()}"
)

print(
    f"Missing Revenue Rows: "
    f"{df['arr_usd'].isna().sum()}"
)


# =====================================================
# Date Standardization
# =====================================================

print("\n===== DATE STANDARDIZATION =====\n")

df["published_date_std"] = (
    df["published_date"]
    .apply(parse_date)
)

df["year"] = (
    df["published_date_std"]
    .dt.year
)

df["month"] = (
    df["published_date_std"]
    .dt.month
)

df["quarter"] = (
    "Q"
    + df["published_date_std"]
        .dt.quarter
        .astype("Int64")
        .astype(str)
)

print(
    f"Failed Dates: "
    f"{df['published_date_std'].isna().sum()}"
)


# =====================================================
# Category Standardization
# =====================================================

print("\n===== CATEGORY STANDARDIZATION =====\n")

df["category_standardized"] = (
    df["category"]
    .apply(standardize_category)
)

print(
    df["category_standardized"]
    .value_counts()
)


# =====================================================
# Company Name Matching
# =====================================================

print("\n===== COMPANY MATCHING =====\n")

df["company_name"] = (
    df["company_name"]
    .apply(normalize_company_name)
)

print("Company Alias Mapping Applied")


# =====================================================
# Load Company Metadata
# =====================================================

print("\n===== COMPANY METADATA =====\n")

with open(
    json_path,
    "r",
    encoding="utf-8"
) as f:

    company_metadata = json.load(f)

company_df = pd.DataFrame.from_dict(
    company_metadata,
    orient="index"
).reset_index()

company_df.rename(
    columns={
        "index": "company_name"
    },
    inplace=True
)

print(
    f"Company Metadata Records: "
    f"{len(company_df)}"
)


# =====================================================
# Merge Metadata
# =====================================================

print("\n===== COMPANY ENRICHMENT =====\n")

df = df.merge(
    company_df,
    on="company_name",
    how="left"
)

df["company_age"] = (
    df["year"]
    - df["founded_year"]
)

df["company_size_category"] = (
    df["employee_count"]
    .apply(get_company_size)
)

print(
    f"Matched Companies: "
    f"{df['founded_year'].notna().sum()}"
)

print(
    f"Unmatched Companies: "
    f"{df['founded_year'].isna().sum()}"
)


# =====================================================
# Remaining Unmatched Companies
# =====================================================

# =====================================================
# Remaining Unmatched Companies
# =====================================================

print("\n===== UNMATCHED COMPANIES =====\n")

unmatched_companies = (
    df[
        df["founded_year"].isna()
    ][["company_name"]]
    .drop_duplicates()
    .sort_values("company_name")
)

print(
    unmatched_companies["company_name"]
    .tolist()
)

# Export unmatched companies

unmatched_output = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "unmatched_companies.csv"
)

unmatched_companies.to_csv(
    unmatched_output,
    index=False
)

print(
    f"Unmatched companies saved to: "
    f"{unmatched_output}"
)


# =====================================================
# Data Quality Checks
# =====================================================

print("\n===== DATA QUALITY =====\n")

print(
    f"Total Rows: {len(df)}"
)

print(
    f"Revenue Missing: "
    f"{df['arr_usd'].isna().sum()}"
)

print(
    f"Date Missing: "
    f"{df['published_date_std'].isna().sum()}"
)

print(
    f"Metadata Missing: "
    f"{df['founded_year'].isna().sum()}"
)


# =====================================================
# Save Silver Layer
# =====================================================

print("\n===== SAVING SILVER DATASET =====\n")

df.to_csv(
    silver_path,
    index=False
)

print(
    f"Saved: {silver_path}"
)


# =====================================================
# Sample Output
# =====================================================

print("\n===== SAMPLE DATA =====\n")

print(
    df[
        [
            "article_id",
            "company_name",
            "arr_usd",
            "published_date_std",
            "category_standardized",
            "company_age",
            "company_size_category"
        ]
    ]
    .head(10)
)