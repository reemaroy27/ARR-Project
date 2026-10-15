from transformations.company_enricher import (
    get_company_size
)


def test_small_company():
    assert get_company_size(9999) == "Small"


def test_medium_lower_boundary():
    assert get_company_size(10000) == "Medium"


def test_medium_upper_boundary():
    assert get_company_size(30000) == "Medium"


def test_large_company():
    assert get_company_size(30001) == "Large"