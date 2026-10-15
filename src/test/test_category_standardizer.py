from transformations.category_standardizer import (
    standardize_category
)


def test_ai_ml():
    assert (
        standardize_category("AI/ML")
        == "AI_ML"
    )


def test_artificial_intelligence():
    assert (
        standardize_category(
            "Artificial Intelligence"
        )
        == "AI_ML"
    )


def test_machine_learning():
    assert (
        standardize_category(
            "Machine Learning"
        )
        == "AI_ML"
    )


def test_cloud_services():
    assert (
        standardize_category(
            "Cloud Services"
        )
        == "CLOUD"
    )


def test_finance():
    assert (
        standardize_category("Finance")
        == "FINTECH"
    )


def test_infosec():
    assert (
        standardize_category("InfoSec")
        == "CYBERSECURITY"
    )
