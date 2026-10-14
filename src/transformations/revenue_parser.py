import re
import pandas as pd

from config.constants import (
    CURRENCY_RATES,
    INVALID_REVENUE_VALUES
)


def detect_currency(value):
    """
    Detect currency from revenue string.
    """

    if "EUR" in value or "€" in value:
        return "EUR"

    if "GBP" in value or "£" in value:
        return "GBP"

    if "JPY" in value or "¥" in value:
        return "JPY"

    return "USD"


def parse_revenue(value):
    """
    Convert revenue formats into USD integer values.
    """

    # Null values
    if pd.isna(value):
        return None

    # Fix encoding issues
    value = str(value).strip()

    value = (
        value
        .replace("â‚¬", "€")
        .replace("Â£", "£")
        .replace("Â¥", "¥")
    )

    # Invalid values
    if value in INVALID_REVENUE_VALUES:
        return None

    currency = detect_currency(value)
    fx_rate = CURRENCY_RATES[currency]

    # -----------------------
    # Range Values
    # Example:
    # $0.982B - $1.086B
    # $57950.0M - $64050.0M
    # -----------------------
    if "-" in value:

        numbers = re.findall(r"\d+\.?\d*", value)

        if len(numbers) >= 2:

            low = float(numbers[0])
            high = float(numbers[1])

            midpoint = (low + high) / 2

            if "B" in value:
                return int(
                    midpoint * 1_000_000_000 * fx_rate
                )

            if "M" in value:
                return int(
                    midpoint * 1_000_000 * fx_rate
                )

    # -----------------------
    # Billion
    # Example:
    # $80.730 billion
    # -----------------------
    if "billion" in value.lower():

        number = float(
            re.findall(r"\d+\.?\d*", value)[0]
        )

        return int(
            number * 1_000_000_000 * fx_rate
        )

    # -----------------------
    # Million
    # Example:
    # $25.6 million
    # -----------------------
    if "million" in value.lower():

        number = float(
            re.findall(r"\d+\.?\d*", value)[0]
        )

        return int(
            number * 1_000_000 * fx_rate
        )

    # -----------------------
    # B notation
    # Example:
    # $96.900B
    # -----------------------
    if "B" in value:

        number = float(
            re.findall(r"\d+\.?\d*", value)[0]
        )

        return int(
            number * 1_000_000_000 * fx_rate
        )

    # -----------------------
    # M notation
    # Example:
    # $450M
    # -----------------------
    if "M" in value:

        number = float(
            re.findall(r"\d+\.?\d*", value)[0]
        )

        return int(
            number * 1_000_000 * fx_rate
        )

    # -----------------------
    # Full Currency Amount
    # Example:
    # $1,785,000,000
    # -----------------------
    cleaned = re.sub(
        r"[^\d.]",
        "",
        value
    )

    try:
        return int(float(cleaned) * fx_rate)

    except (ValueError, TypeError):
        return None