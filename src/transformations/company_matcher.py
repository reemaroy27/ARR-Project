from config.constants import (COMPANY_ALIASES)

def normalize_company_name(company_name: str) -> str:
    return COMPANY_ALIASES.get(
        company_name,
        company_name
    )

def get_match_method(company_name: str) -> str:

    if company_name in COMPANY_ALIASES:
        return "MATCHED_ALIAS"

    return "MATCHED_EXACT"