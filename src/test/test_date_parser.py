import pandas as pd

from transformations.date_parser import parse_date


def test_iso_date():
    result = parse_date("2022-02-17")
    assert result == pd.Timestamp("2022-02-17")


def test_iso_timestamp():
    result = parse_date("2021-09-11T00:00:00Z")
    assert result == pd.Timestamp("2021-09-11")


def test_text_date():
    result = parse_date("October 19, 2022")
    assert result == pd.Timestamp("2022-10-19")


def test_us_date():
    result = parse_date("02/23/2023")
    assert result == pd.Timestamp("2023-02-23")


def test_eu_date():
    result = parse_date("23-08-2023")
    assert result == pd.Timestamp("2023-08-23")


def test_missing_date():
    assert pd.isna(parse_date(None))


def test_invalid_date():
    assert pd.isna(parse_date("invalid-date"))

def test_ambiguous_slash_date():
    result = parse_date("04/05/2023")
    assert result == pd.Timestamp("2023-04-05")