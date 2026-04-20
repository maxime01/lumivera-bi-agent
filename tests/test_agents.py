"""
Tests sans appel API — 0 crédit consommé.
Tous les appels LLM sont mockés.
"""
import json
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest


# ── Schema ────────────────────────────────────────────────────────────────────

def test_schema_contains_table_name():
    from src.schema import SCHEMA_TEXT, TABLE_NAME
    assert TABLE_NAME in SCHEMA_TEXT

def test_schema_contains_key_columns():
    from src.schema import SCHEMA_TEXT
    for col in ("period", "country", "sku_code", "forecast_qty", "actual_qty", "channel"):
        assert col in SCHEMA_TEXT


# ── Orchestrator ──────────────────────────────────────────────────────────────

def test_orchestrator_returns_dict():
    mock_json = json.dumps({
        "sql_needed": True,
        "sql_intent": "MAPE par pays",
        "analysis_focus": "outliers MAPE > 30%",
        "domain_context": "pays",
    })
    with patch("src.orchestrator.call_claude", return_value=mock_json):
        from src.orchestrator import plan
        result = plan("Quel est le MAPE par pays ?")
    assert isinstance(result, dict)
    assert result["sql_needed"] is True
    assert "sql_intent" in result

def test_orchestrator_fallback_on_bad_json():
    with patch("src.orchestrator.call_claude", return_value="pas du JSON valide"):
        from src.orchestrator import plan
        result = plan("question quelconque")
    assert result["sql_needed"] is True


# ── SQL Executor ──────────────────────────────────────────────────────────────

def test_sql_executor_strips_semicolon_and_readds():
    mock_sql = "SELECT country, ROUND(AVG(ABS(actual_qty-forecast_qty)*1.0/NULLIF(forecast_qty,0))*100,2) AS mape FROM forecast_vs_actuals GROUP BY 1 LIMIT 20"
    mock_df = pd.DataFrame([{"country": "FR", "mape": 12.5}])

    with patch("src.sql_executor.call_claude", return_value=mock_sql), \
         patch("src.sql_executor.run_query_df", return_value=mock_df):
        from src.sql_executor import generate_and_run
        sql, df = generate_and_run("MAPE par pays")

    assert sql.endswith(";")
    assert df is not None
    assert "country" in df.columns

def test_sql_executor_handles_db_error():
    with patch("src.sql_executor.call_claude", return_value="SELECT bad sql"), \
         patch("src.sql_executor.run_query_df", side_effect=Exception("syntax error")):
        from src.sql_executor import generate_and_run
        sql, df = generate_and_run("question")
    assert df is None


# ── Data Analyst ──────────────────────────────────────────────────────────────

def test_data_analyst_no_data_returns_message():
    from src.data_analyst import analyze
    result = analyze("question", "SELECT 1", None, "focus")
    assert "Aucune donnée" in result

def test_data_analyst_with_data_calls_llm():
    df = pd.DataFrame([{"country": "FR", "mape": 12.5}, {"country": "UK", "mape": 22.1}])
    with patch("src.data_analyst.call_claude", return_value="• FR MAPE 12.5% — performance correcte"):
        from src.data_analyst import analyze
        result = analyze("MAPE par pays ?", "SELECT ...", df, "anomalies")
    assert isinstance(result, str)
    assert len(result) > 0


# ── Domain Expert ─────────────────────────────────────────────────────────────

def test_domain_expert_returns_string():
    with patch("src.domain_expert.call_claude", return_value="Le pic de décembre s'explique par les fêtes."):
        from src.domain_expert import enrich
        result = enrich("MAPE par pays ?", "FR MAPE 12%", "pays")
    assert isinstance(result, str)


# ── Viz Formatter ─────────────────────────────────────────────────────────────

def test_viz_formatter_returns_formatted_response():
    expected = "## Réponse\nLe MAPE moyen est de 15%."
    with patch("src.viz_formatter.call_claude", return_value=expected):
        from src.viz_formatter import format_output
        result = format_output("MAPE ?", "analyse", "contexte", None)
    assert "## Réponse" in result

def test_viz_formatter_includes_data_preview():
    df = pd.DataFrame([{"country": "FR", "mape": 12.5}])
    captured = {}

    def mock_call(system, user, **kwargs):
        captured["user"] = user
        return "## Réponse\nOK"

    with patch("src.viz_formatter.call_claude", side_effect=mock_call):
        from src.viz_formatter import format_output
        format_output("MAPE ?", "analyse", "contexte", df)

    assert "FR" in captured["user"]
