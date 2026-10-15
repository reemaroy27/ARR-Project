from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent

duckdb_path = (
    PROJECT_ROOT
    / "data"
    / "gold"
    / "warehouse.duckdb"
)

conn = duckdb.connect(str(duckdb_path))

print("\n===== TABLES =====\n")

print(
    conn.execute(
        "SHOW TABLES"
    ).fetchall()
)

print("\n===== DIM COMPANY =====\n")

print(
    conn.execute(
        "DESCRIBE dim_company"
    ).fetchdf()
)

print("\n===== FACT ARR =====\n")

print(
    conn.execute(
        "DESCRIBE fact_arr_observation"
    ).fetchdf()
)

conn.close()