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

output_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_with_embeddings.csv"
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
# Save
# ============================================

df.to_csv(
    output_path,
    index=False
)

print(f"Saved: {output_path}")