"""
Lumivera BI Agent — point d'entrée
POC Multi-Agent BI Orchestrator | Stack : Python + Anthropic API + DuckDB
"""
import json
import sys

from dotenv import load_dotenv
load_dotenv()

from src.orchestrator import plan
from src.sql_executor import generate_and_run
from src.data_analyst import analyze
from src.domain_expert import enrich
from src.viz_formatter import format_output


def run(question: str) -> str:
    print(f"\n{'═'*60}")
    print(f"❓ {question}")
    print("═" * 60)

    # Agent 1 — Orchestrateur
    print("\n[1/5] 🧠 Orchestrateur — analyse la question...")
    execution_plan = plan(question)
    print(f"      Plan → {json.dumps(execution_plan, ensure_ascii=False, indent=2)}")

    # Agent 2 — SQL Executor
    sql, data = None, None
    if execution_plan.get("sql_needed", True):
        print("\n[2/5] 🗄️  SQL Executor — génère et exécute la requête...")
        sql, data = generate_and_run(execution_plan.get("sql_intent", question))
        print(f"      SQL → {sql}")
        print(f"      Résultat → {len(data) if data is not None else 0} lignes")

    # Agent 3 — Data Analyst
    print("\n[3/5] 📊 Data Analyst — interprète les résultats...")
    analysis = analyze(
        question, sql or "", data,
        focus=execution_plan.get("analysis_focus", ""),
    )

    # Agent 4 — Domain Expert
    print("\n[4/5] 💼 Domain Expert — ajoute le contexte métier...")
    expertise = enrich(
        question, analysis,
        context=execution_plan.get("domain_context", ""),
    )

    # Agent 5 — Viz Formatter
    print("\n[5/5] 🎨 Viz Formatter — formate la réponse finale...")
    final = format_output(question, analysis, expertise, data)

    print("\n" + "─" * 60)
    print(final)
    print("─" * 60)
    return final


DEMO_QUESTIONS = [
    "Quel est le MAPE par pays sur 2024 ?",
    "Y a-t-il des anomalies dans les ventes sur la période ?",
    "Quelle est la tendance mensuelle du SKU TEST0001 ?",
    "Quel canal performe le mieux en termes d'écart forecast vs actual ?",
]

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEMO_QUESTIONS[0]
    run(question)
