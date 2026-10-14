from transformations.revenue_parser import parse_revenue

def test_million():
    assert parse_revenue("$980M") == 980000000

def test_billion():
    assert parse_revenue("$5.2B") == 5200000000

def test_range():
    assert parse_revenue("$90M-$100M") == 95000000

def test_null_value():
    assert parse_revenue("N/A") is None

def test_eur_conversion():
    assert parse_revenue("€1,000,000") == 1100000


def test_gbp_conversion():
    assert parse_revenue("£100,000,000") == 127000000


def test_jpy_conversion():
    assert parse_revenue("¥150,000,000") == 1000000