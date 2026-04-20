"""
Schéma partagé entre tous les agents.
Source de vérité unique — modifier ici pour tous.
"""

TABLE_NAME = "forecast_vs_actuals"

SCHEMA_TEXT = f"""
Table : {TABLE_NAME}
  period          DATE    -- mois (ex : 2023-01-01)
  country         STRING  -- FR, UK, AU, US, DE
  brand           STRING  -- toujours 'Lumivera'
  category        STRING  -- Skincare, Haircare, Makeup
  sku_code        STRING  -- TEST0001 à TEST0010
  sku_label       STRING  -- libellé produit
  forecast_qty    INT     -- unités prévues
  actual_qty      INT     -- ventes réelles
  forecast_value  FLOAT   -- CA prévu (€)
  actual_value    FLOAT   -- CA réel (€)
  channel         STRING  -- Retail, E-commerce, Travel Retail, Pharmacy
  demand_planner  STRING  -- Alice Martin, Ben Okoro, Clara Voss
"""
