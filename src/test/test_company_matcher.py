from transformations.company_matcher import (
    normalize_company_name,
    get_match_method
)


def test_aws_alias():
    assert (
        normalize_company_name("AWS")
        == "Amazon Web Services"
    )


def test_openai_alias():
    assert (
        normalize_company_name("Open AI")
        == "OpenAI"
    )


def test_mongodb_alias():
    assert (
        normalize_company_name("Mongo DB")
        == "MongoDB"
    )


def test_exact_match():
    assert (
        normalize_company_name("OpenAI")
        == "OpenAI"
    )


def test_alias_match_method():
    assert (
        get_match_method("AWS")
        == "MATCHED_ALIAS"
    )


def test_exact_match_method():
    assert (
        get_match_method("OpenAI")
        == "MATCHED_EXACT"
    )

def test_unresolved_company():
    assert (
        normalize_company_name("Some Random Startup")
        == "Some Random Startup"
    )