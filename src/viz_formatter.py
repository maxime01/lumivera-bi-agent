"""Agent 5 — Viz Formatter : réponse structurée lisible pour un non-technique."""
from __future__ import annotations
import pandas as pd

from .llm import call_claude

_SYSTEM = """Tu es un expert en communication business.
Produis une réponse structurée pour un demand planner non technique.

Format OBLIGATOIRE :
## Réponse
[Réponse directe en 1-2 phrases]

### Points clés
[3 à 5 bullets avec chiffres]

### Actions recommandées
[1 à 2 actions concrètes]

Français simple, zéro jargon technique."""


def format_output(
    question: str,
    analysis: str,
    expertise: str,
    data: pd.DataFrame | None,
) -> str:
    data_preview = ""
    if data is not None and not data.empty:
        data_preview = "\n\nDonnées clés :\n" + data.head(10).to_string(index=False)

    user = f"""Question : {question}

Analyse data :
{analysis}

Contexte expert :
{expertise}
{data_preview}"""

    return call_claude(_SYSTEM, user, max_tokens=600)
