from config.constants import (CATEGORY_MAPPING)

def standardize_category(category):

    if category is None:
        return None

    return CATEGORY_MAPPING.get(
        category,
        category
    )