"""
Agent 2 — SQL Executor
Traduit un intent en SQL DuckDB et l'exécute sur le CSV.
"""
import pandas as pd

from .llm import call_claude
from .schema import SCHEMA_TEXT, TABLE_NAME
from .database import run_query_df

_SYSTEM = f"""Tu es un expert SQL (dialecte DuckDB).
Génère UNE SEULE requête SQL valide. Retourne UNIQUEMENT le SQL, sans markdown ni backticks.

Règles :
- Table cible : {TABLE_NAME}
- Groupement mensuel : strftime('%Y-%m', period)
- MAPE : AVG(ABS(actual_qty - forecast_qty) * 1.0 / NULLIF(forecast_qty, 0)) * 100
- Toujours LIMIT 20
- ROUND(x, 2) sur les floats

Schéma :
{SCHEMA_TEXT}"""


def generate_and_run(intent: str) -> tuple[str, pd.DataFrame | None]:
    sql = call_claude(_SYSTEM, f"Intent : {intent}", max_tokens=600).rstrip(";") + ";"
    try:
        return sql, run_query_df(sql)
    except Exception as e:
        print(f"      [SQL ERROR] {e}")
        return sql, None
