from pathlib import Path
import ast

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

input_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_with_embeddings.csv"
)

# =====================================================
# Load Data
# =====================================================

df = pd.read_csv(input_path)

# Convert embedding strings back into Python lists
df["embedding"] = df["embedding"].apply(ast.literal_eval)

# Create year column from published_date
df["published_date"] = pd.to_datetime(
    df["published_date"],
    errors="coerce"
)

df["year"] = df["published_date"].dt.year

print(f"Loaded {len(df)} articles")
print("\nColumns:")
print(df.columns.tolist())

# =====================================================
# Load Model
# =====================================================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Model Loaded")

# =====================================================
# Hybrid Search
# =====================================================

def find_hybrid_articles(query_text, top_k=5):
    """
    Hybrid Search:
    1. Apply business filters
    2. Run semantic similarity search
    """

    filtered_df = df[
        (
            (df["category"] == "AI_ML")
            | (df["industry"] == "AI/ML")
        )
        & (df["year"] >= 2022)
        & (df["year"] <= 2024)
        & (df["arr_usd"].fillna(0) > 50_000_000)
    ].copy()

    if filtered_df.empty:
        print("No records match the filter criteria.")
        return pd.DataFrame()

    query_embedding = model.encode([query_text])

    article_embeddings = filtered_df[
        "embedding"
    ].tolist()

    scores = cosine_similarity(
        query_embedding,
        article_embeddings
    )[0]

    filtered_df["similarity_score"] = scores

    return (
        filtered_df
        .sort_values(
            "similarity_score",
            ascending=False
        )[
            [
                "article_id",
                "title",
                "company_name",
                "industry",
                "arr_usd",
                "similarity_score"
            ]
        ]
        .head(top_k)
    )

# =====================================================
# Example Queries
# =====================================================

if __name__ == "__main__":

    queries = [
        "large language model funding",
        "AI startup fundraising",
        "cloud revenue growth",
        "enterprise AI platform"
    ]

    for query in queries:

        print("\n" + "=" * 60)
        print(f"\nQUERY: {query}\n")

        results = find_hybrid_articles(query)

        if not results.empty:
            print(results.to_string(index=False))
        else:
            print("No matching articles found.")