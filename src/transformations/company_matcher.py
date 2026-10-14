from config.constants import (COMPANY_ALIASES)

def normalize_company_name(company_name: str) -> str:

    return COMPANY_ALIASES.get(
        company_name,
        company_name
    )