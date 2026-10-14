from pathlib import Path
import ast

import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parent.parent

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

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
##################################
def find_similar_articles(
    query_text,
    top_k=5
):
    query_embedding = model.encode(
        [query_text]
    )

    article_embeddings = df["embedding"].tolist()

    scores = cosine_similarity(
        query_embedding,
        article_embeddings
    )[0]

    result = df.copy()

    result["similarity_score"] = scores

    result = result.sort_values(
        "similarity_score",
        ascending=False
    )

    return result[
        [
            "article_id",
            "title",
            "company_name",
            "similarity_score"
        ]
    ].head(top_k)
#####################################
if __name__ == "__main__":

    results = find_similar_articles(
        "large language model funding"
    )

    print(results)