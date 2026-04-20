"""
DuckDB sur CSV local.
Pour passer en prod BigQuery : remplacer get_connection() et run_query_df()
par google.cloud.bigquery.Client() + client.query(sql).to_dataframe().
"""
import os
from pathlib import Path

import duckdb
import pandas as pd

from .schema import TABLE_NAME

_conn: duckdb.DuckDBPyConnection | None = None
_CSV_DEFAULT = Path(__file__).parent.parent / "data" / "forecast_vs_actuals_v2.csv"


def get_connection() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is None:
        csv_path = os.getenv("LUMIVERA_CSV", str(_CSV_DEFAULT))
        if not Path(csv_path).exists():
            raise FileNotFoundError(
                f"Dataset introuvable : {csv_path}\n"
                "Déposer forecast_vs_actuals_v2.csv dans data/ ou définir LUMIVERA_CSV."
            )
        df = pd.read_csv(csv_path)
        _conn = duckdb.connect()
        _conn.register(TABLE_NAME, df)
    return _conn


def run_query_df(sql: str) -> pd.DataFrame:
    return get_connection().execute(sql).df()
