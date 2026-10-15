import pandas as pd
from typing import Optional

def get_company_size(employee_count: float) -> Optional[str]:

    if pd.isna(employee_count):
        return None

    if employee_count < 10000:
        return "Small"

    if employee_count <= 30000:
        return "Medium"

    return "Large"