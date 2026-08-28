# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.scenario_registry (
# MAGIC     scenario_id STRING,
# MAGIC     scenario_name STRING,
# MAGIC     scenario_type STRING,
# MAGIC
# MAGIC     target_component STRING,
# MAGIC     change_description STRING,
# MAGIC
# MAGIC     baseline_mass_g DOUBLE,
# MAGIC     scenario_mass_g DOUBLE,
# MAGIC     reduction_pct DOUBLE,
# MAGIC
# MAGIC     scenario_basis STRING,
# MAGIC     evidence_classification STRING,
# MAGIC
# MAGIC     reviewer_note STRING,
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO kraft_heinz_lca.gold.scenario_registry
# MAGIC VALUES (
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC     'LIGHTWEIGHTING',
# MAGIC
# MAGIC     'Bottle',
# MAGIC     'Reduce PET bottle mass by 10% while holding other modeled components constant.',
# MAGIC
# MAGIC     30.0,
# MAGIC     27.0,
# MAGIC     10.0,
# MAGIC
# MAGIC     'Learning scenario informed by Kraft Heinz material-reduction strategy; exact 10% reduction is not company-reported for this SKU.',
# MAGIC     'SYNTHETIC_SCENARIO_ASSUMPTION',
# MAGIC
# MAGIC     'Use for scenario modeling only. Product protection, bottle performance, filling-line compatibility, shelf life and consumer functionality are assumed unchanged for this first sensitivity test.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH baseline AS (
# MAGIC     SELECT
# MAGIC         packaging_component,
# MAGIC         component_mass_kg,
# MAGIC         impact_result
# MAGIC     FROM kraft_heinz_lca.gold.lca_results
# MAGIC     WHERE model_id = 'OLCA-KH-S0-001'
# MAGIC       AND impact_category = 'Global warming'
# MAGIC ),
# MAGIC
# MAGIC scenario AS (
# MAGIC     SELECT
# MAGIC         packaging_component,
# MAGIC
# MAGIC         CASE
# MAGIC             WHEN packaging_component = 'Bottle'
# MAGIC             THEN component_mass_kg * 0.90
# MAGIC             ELSE component_mass_kg
# MAGIC         END AS scenario_mass_kg,
# MAGIC
# MAGIC         CASE
# MAGIC             WHEN packaging_component = 'Bottle'
# MAGIC             THEN impact_result * 0.90
# MAGIC             ELSE impact_result
# MAGIC         END AS scenario_gwp_kg_co2e
# MAGIC
# MAGIC     FROM baseline
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     SUM(scenario_mass_kg) AS s1_modeled_mass_kg,
# MAGIC     SUM(scenario_gwp_kg_co2e) AS s1_gwp_kg_co2e
# MAGIC FROM scenario;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_results
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'LCA-S1-GWP-PET',
# MAGIC     'OLCA-KH-S1-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC     1.0,
# MAGIC
# MAGIC     'COMP-BOTTLE',
# MAGIC     'Bottle',
# MAGIC
# MAGIC     0.027,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.05801,
# MAGIC     58.67,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     '10% PET bottle mass reduction scenario. Bottle forming, filling, label, distribution, and end-of-life excluded.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'LCA-S1-GWP-CASE',
# MAGIC     'OLCA-KH-S1-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC     1.0,
# MAGIC
# MAGIC     'COMP-CASE',
# MAGIC     'Corrugated case allocation',
# MAGIC
# MAGIC     0.018,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.03275,
# MAGIC     33.13,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     'Containerboard proxy unchanged from baseline.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'LCA-S1-GWP-PP',
# MAGIC     'OLCA-KH-S1-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC     1.0,
# MAGIC
# MAGIC     'COMP-CAP',
# MAGIC     'Cap',
# MAGIC
# MAGIC     0.004,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.00811,
# MAGIC     8.20,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     'PP cap unchanged from baseline.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     SUM(component_mass_kg) AS modeled_mass_kg,
# MAGIC     SUM(impact_result) AS total_gwp_kg_co2e,
# MAGIC     SUM(contribution_pct) AS contribution_pct
# MAGIC FROM kraft_heinz_lca.gold.lca_results
# MAGIC WHERE scenario_id IN ('S0','S1')
# MAGIC   AND impact_category = 'Global warming'
# MAGIC GROUP BY scenario_id
# MAGIC ORDER BY scenario_id;