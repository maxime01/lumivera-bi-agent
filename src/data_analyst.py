"""Agent 3 — Data Analyst : interprète les résultats SQL (tendances, anomalies, MAPE)."""
from __future__ import annotations
import pandas as pd

from .llm import call_claude

_SYSTEM = """Tu es un data analyst senior spécialisé en demand planning FMCG.
Extrais les 3 à 5 insights quantitatifs les plus importants.
Mets en avant les anomalies, tendances et outliers.
Cite toujours des chiffres précis. Réponds en français."""


def analyze(question: str, sql: str, data: pd.DataFrame | None, focus: str) -> str:
    if data is None or data.empty:
        return "Aucune donnée disponible pour cette analyse."

    user = f"""Question : {question}
Focus : {focus}

SQL exécuté :
{sql}

Résultats :
{data.to_string(index=False, max_rows=20)}"""

    return call_claude(_SYSTEM, user, max_tokens=600)
