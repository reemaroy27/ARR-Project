import pandas as pd

def parse_date(date_value):

    if pd.isna(date_value):
        return pd.NaT

    formats = [
        "%d-%b-%y",
        "%d-%b-%Y",
        "%d %b %Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%SZ",
        "%m-%d-%Y"
    ]

    for fmt in formats:

        try:
            return pd.to_datetime(
                date_value,
                format=fmt
            )

        except ValueError:
            continue

    return pd.NaT