def test_million():
    assert parse_revenue("$980M") == 980000000

def test_billion():
    assert parse_revenue("$5.2B") == 5200000000

def test_range():
    assert parse_revenue("$90M-$100M") == 95000000

def test_null_value():
    assert parse_revenue("N/A") is None