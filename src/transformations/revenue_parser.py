import re
from typing import Optional

import pandas as pd

from config.constants import (
    CURRENCY_RATES,
    INVALID_REVENUE_VALUES
)


def get_parse_status(
    raw_value,
    parsed_value
) -> str:
    """
    Determine revenue parse status.

    SUCCESS:
        Revenue successfully parsed.

    MISSING:
        Revenue unavailable, null, N/A,
        Not disclosed, etc.

    FAILED:
        Revenue provided but could not
        be parsed.
    """

    if pd.isna(raw_value):
        return "MISSING"

    normalized_invalids = {
        str(v).strip().lower()
        for v in INVALID_REVENUE_VALUES
        if v is not None
    }

    if (
        str(raw_value)
        .strip()
        .lower()
        in normalized_invalids
    ):
        return "MISSING"

    if pd.isna(parsed_value):
        return "FAILED"

    return "SUCCESS"


def detect_currency(value: str) -> str:
    """
    Detect currency from revenue string.
    """

    value_upper = value.upper()

    if "EUR" in value_upper or "€" in value:
        return "EUR"

    if "GBP" in value_upper or "£" in value:
        return "GBP"

    if "JPY" in value_upper or "¥" in value:
        return "JPY"

    return "USD"


def extract_number(
    value: str
) -> Optional[float]:
    """
    Extract first numeric value from text.

    Examples:
        "$5.2B" -> 5.2
        "80.730 billion" -> 80.730
    """

    matches = re.findall(
        r"\d+\.?\d*",
        value
    )

    if not matches:
        return None

    return float(matches[0])


def parse_revenue(
    value: str
) -> Optional[int]:
    """
    Convert revenue formats into USD integer values.

    Supports:

    - $980M
    - $5.2B
    - 500M USD
    - $80.730 billion
    - $455.0 million
    - €1,254,545,455
    - £244,094,488
    - ¥360,000,000,000
    - $90M - $100M
    """

    # ---------------------------------------
    # Missing values
    # ---------------------------------------

    if pd.isna(value):
        return None

    value = str(value).strip()

    # Fix encoding issues
    value = (
        value
        .replace("â‚¬", "€")
        .replace("Â£", "£")
        .replace("Â¥", "¥")
    )

    normalized_invalids = {
        str(v).strip().lower()
        for v in INVALID_REVENUE_VALUES
        if v is not None
    }

    if value.lower() in normalized_invalids:
        return None

    currency = detect_currency(value)
    fx_rate = CURRENCY_RATES[currency]

    value_upper = value.upper()

    # ---------------------------------------
    # Revenue ranges
    # ---------------------------------------

    if "-" in value:

        numbers = re.findall(
            r"\d+\.?\d*",
            value
        )

        if len(numbers) >= 2:

            low = float(numbers[0])
            high = float(numbers[1])

            midpoint = (low + high) / 2

            if "B" in value_upper:
                return int(
                    midpoint *
                    1_000_000_000 *
                    fx_rate
                )

            if "M" in value_upper:
                return int(
                    midpoint *
                    1_000_000 *
                    fx_rate
                )

    # ---------------------------------------
    # Billion text
    # ---------------------------------------

    if "billion" in value.lower():

        number = extract_number(value)

        if number is None:
            return None

        return int(
            number *
            1_000_000_000 *
            fx_rate
        )

    # ---------------------------------------
    # Million text
    # ---------------------------------------

    if "million" in value.lower():

        number = extract_number(value)

        if number is None:
            return None

        return int(
            number *
            1_000_000 *
            fx_rate
        )

    # ---------------------------------------
    # B notation
    # ---------------------------------------

    if "B" in value_upper:

        number = extract_number(value)

        if number is None:
            return None

        return int(
            number *
            1_000_000_000 *
            fx_rate
        )

    # ---------------------------------------
    # M notation
    # ---------------------------------------

    if "M" in value_upper:

        number = extract_number(value)

        if number is None:
            return None

        return int(
            number *
            1_000_000 *
            fx_rate
        )

    # ---------------------------------------
    # Full currency amount
    # ---------------------------------------

    cleaned = re.sub(
        r"[^\d.]",
        "",
        value
    )

    try:
        return int(
            float(cleaned) *
            fx_rate
        )

    except (ValueError, TypeError):
        return None