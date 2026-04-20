"""
Agent 4 — Domain Expert
Ajoute le contexte métier cosmétiques / supply chain à l'analyse chiffrée.
"""
from .llm import call_claude

_SYSTEM = """Tu es un demand planning expert avec 15 ans d'expérience en cosmétique FMCG.
À partir d'une analyse chiffrée, tu ajoutes le contexte business :
- Pourquoi ces chiffres (saisonnalité, promo, rupture, lancement…)
- Ce sur quoi le demand planner doit agir
- 1 ou 2 actions concrètes
Sois bref (3-4 phrases). Réponds en français."""


def enrich(question: str, analysis: str, context: str) -> str:
    user = f"""Question : {question}
Contexte : {context}

Analyse :
{analysis}"""

    return call_claude(_SYSTEM, user, max_tokens=350)
