"""
Agent 1 — Orchestrateur
Analyse la question utilisateur et produit un plan JSON pour les autres agents.
"""
import json

from .llm import call_claude
from .schema import SCHEMA_TEXT

_SYSTEM = f"""Tu es l'orchestrateur d'un système BI multi-agent.
Reçois une question utilisateur et retourne UNIQUEMENT un objet JSON valide (sans markdown) :
{{
  "sql_needed"    : true ou false,
  "sql_intent"    : "ce que la requête SQL doit calculer (null si pas de SQL)",
  "analysis_focus": "ce que le data analyst doit chercher dans les résultats",
  "domain_context": "dimension métier principale (pays, catégorie, canal, SKU…)"
}}

Schéma de données :
{SCHEMA_TEXT}"""


def plan(question: str) -> dict:
    raw = call_claude(_SYSTEM, question, cache_system=True, fast=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "sql_needed": True,
            "sql_intent": question,
            "analysis_focus": question,
            "domain_context": "general",
        }
