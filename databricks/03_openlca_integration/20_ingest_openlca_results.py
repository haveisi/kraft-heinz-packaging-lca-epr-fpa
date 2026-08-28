# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.lca_results (
# MAGIC     result_id STRING,
# MAGIC
# MAGIC     model_id STRING,
# MAGIC     sku_id STRING,
# MAGIC     scenario_id STRING,
# MAGIC     scenario_name STRING,
# MAGIC
# MAGIC     functional_unit STRING,
# MAGIC     functional_unit_amount DOUBLE,
# MAGIC
# MAGIC     component_id STRING,
# MAGIC     packaging_component STRING,
# MAGIC
# MAGIC     component_mass_kg DOUBLE,
# MAGIC
# MAGIC     impact_method STRING,
# MAGIC     impact_category STRING,
# MAGIC     impact_unit STRING,
# MAGIC
# MAGIC     impact_result DOUBLE,
# MAGIC     contribution_pct DOUBLE,
# MAGIC
# MAGIC     result_source STRING,
# MAGIC     result_status STRING,
# MAGIC
# MAGIC     model_boundary STRING,
# MAGIC     limitation_note STRING,
# MAGIC
# MAGIC     calculated_at TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_results
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'LCA-S0-GWP-PET',
# MAGIC     'OLCA-KH-S0-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S0',
# MAGIC     'Baseline',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC     1.0,
# MAGIC
# MAGIC     'COMP-BOTTLE',
# MAGIC     'Bottle',
# MAGIC
# MAGIC     0.030,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.06446,
# MAGIC     61.20,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     'PET resin production represented. Bottle forming, filling, distribution, label and end-of-life are not yet included.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'LCA-S0-GWP-CASE',
# MAGIC     'OLCA-KH-S0-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S0',
# MAGIC     'Baseline',
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
# MAGIC     31.10,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     'Containerboard at mill is used as a screening proxy. Corrugating and finished-box conversion are not explicitly represented.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'LCA-S0-GWP-PP',
# MAGIC     'OLCA-KH-S0-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S0',
# MAGIC     'Baseline',
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
# MAGIC     7.70,
# MAGIC
# MAGIC     'openLCA 2.6.1 contribution tree',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging material production',
# MAGIC
# MAGIC     'Virgin PP resin represented. Cap molding/conversion is not yet included.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(component_mass_kg) AS modeled_mass_kg,
# MAGIC     SUM(impact_result) AS summed_gwp_kg_co2e,
# MAGIC     SUM(contribution_pct) AS summed_contribution_pct
# MAGIC FROM kraft_heinz_lca.gold.lca_results
# MAGIC WHERE model_id = 'OLCA-KH-S0-001'
# MAGIC   AND impact_category = 'Global warming';