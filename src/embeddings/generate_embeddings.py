from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer


# ============================================
# Paths
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

input_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_enriched.csv"
)

embeddings_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_with_embeddings.csv"
)

enriched_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_enriched.csv"
)


# ============================================
# Load Data
# ============================================

df = pd.read_csv(input_path)

print(f"Loaded {len(df)} rows")


# ============================================
# Build Text For Embedding
# ============================================

df["embedding_text"] = (
    df["title"].fillna("")
    + " "
    + df["summary"].fillna("")
)


# ============================================
# Load Model
# ============================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model Loaded")


# ============================================
# Generate Embeddings
# ============================================

embeddings = model.encode(
    df["embedding_text"].tolist(),
    show_progress_bar=True
)

df["embedding"] = [
    embedding.tolist()
    for embedding in embeddings
]

print("Embeddings Generated")


# ============================================
# Save Embedding Dataset
# ============================================

df.to_csv(
    embeddings_path,
    index=False
)

print(f"Saved: {embeddings_path}")


# ============================================
# Update Required Export
# ============================================

enriched_df = pd.read_csv(enriched_path)

# Remove existing embedding column if present
if "embedding" in enriched_df.columns:
    enriched_df = enriched_df.drop(
        columns=["embedding"]
    )

enriched_df = enriched_df.merge(
    df[
        [
            "article_id",
            "embedding"
        ]
    ],
    on="article_id",
    how="left"
)

enriched_df.to_csv(
    enriched_path,
    index=False
)

print(
    f"Updated required export: {enriched_path}"
)


# ============================================
# Validation
# ============================================

print("\n===== OUTPUT COLUMNS =====\n")

print(enriched_df.columns.tolist())