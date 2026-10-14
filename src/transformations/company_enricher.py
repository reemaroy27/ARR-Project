import pandas as pd


def get_company_size(employee_count):

    if pd.isna(employee_count):
        return None

    if employee_count < 10000:
        return "Small"

    if employee_count <= 30000:
        return "Medium"

    return "Large"