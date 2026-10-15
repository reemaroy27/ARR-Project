from pathlib import Path
import ast

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

input_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_with_embeddings.csv"
)

df = pd.read_csv(input_path)

df["embedding"] = (
    df["embedding"]
    .apply(ast.literal_eval)
)

embeddings = df["embedding"].tolist()

similarity_matrix = cosine_similarity(
    embeddings
)

neighbors = []

for i in range(len(df)):

    scores = similarity_matrix[i]

    top_indices = (
        scores.argsort()[::-1][1:4]
    )

    neighbor_ids = (
        df.iloc[top_indices]
        ["article_id"]
        .tolist()
    )

    neighbors.append(
        "|".join(neighbor_ids)
    )

df["top_similar_articles"] = neighbors

output_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "ai_articles_with_neighbors.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"Saved: {output_path}"
)