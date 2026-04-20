# Lumivera BI Agent

POC — Multi-Agent BI Orchestrator pour le demand planning cosmétique FMCG.

Pose une question en langage naturel → 5 agents spécialisés génèrent le SQL, interprètent les résultats, ajoutent le contexte métier et produisent une réponse structurée.

## Architecture

```
Question utilisateur
        │
        ▼
[Agent 1] Orchestrateur   — décompose la question, construit le plan d'exécution
        │
        ▼
[Agent 2] SQL Executor    — génère et exécute une requête DuckDB sur le CSV
        │
        ▼
[Agent 3] Data Analyst    — interprète les résultats, détecte anomalies et tendances
        │
        ▼
[Agent 4] Domain Expert   — ajoute le contexte métier FMCG (saisonnalité, canal…)
        │
        ▼
[Agent 5] Viz Formatter   — produit une réponse claire pour un non-technique
```

## Démarrage rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer la clé API
cp .env.example .env
# Éditer .env → ajouter ANTHROPIC_API_KEY

# 3. Déposer le CSV dans data/
cp /chemin/vers/forecast_vs_actuals_v2.csv data/

# 4. Lancer
python main.py "Quel est le MAPE par pays sur 2024 ?"
```

## Questions de démo

```bash
python main.py "Quel est le MAPE par pays sur 2024 ?"
python main.py "Y a-t-il des anomalies dans les ventes sur la période ?"
python main.py "Quelle est la tendance mensuelle du SKU TEST0001 ?"
python main.py "Quel canal performe le mieux en termes d'écart forecast vs actual ?"
```

## Tests (sans appel API)

```bash
pytest tests/ -v
```

Tous les appels LLM sont mockés → 0 crédit consommé.

## Stack

| Couche | Outil |
|--------|-------|
| LLM | Claude `claude-sonnet-4-6` via SDK Anthropic |
| Base de données locale | DuckDB sur CSV |
| Passage en prod | Remplacer `src/database.py` par BigQuery |

## Passage BigQuery

Remplacer dans `src/database.py` :
```python
# Remplacer get_connection() + run_query_df() par :
from google.cloud import bigquery
client = bigquery.Client()
df = client.query(sql).to_dataframe()
```
Tout le reste du pipeline reste identique.
