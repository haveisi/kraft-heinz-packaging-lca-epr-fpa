# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC DESCRIBE TABLE kraft_heinz_lca.gold.lca_scenario_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SHOW COLUMNS IN kraft_heinz_lca.gold.lca_scenario_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC (
# MAGIC     scenario_result_id,
# MAGIC     model_id,
# MAGIC     sku_id,
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     functional_unit,
# MAGIC     modeled_packaging_mass_kg,
# MAGIC     impact_method,
# MAGIC     impact_category,
# MAGIC     impact_unit,
# MAGIC     impact_result,
# MAGIC     baseline_impact_result,
# MAGIC     avoided_impact_per_unit,
# MAGIC     reduction_pct,
# MAGIC     result_source,
# MAGIC     result_status,
# MAGIC     data_classification,
# MAGIC     limitation_note,
# MAGIC     calculated_at
# MAGIC )
# MAGIC
# MAGIC VALUES
# MAGIC (
# MAGIC     'LCA-S3-GWP-001',
# MAGIC     'OLCA-KH-S3-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S3',
# MAGIC     '10% Lightweighting + 30% rPET',
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC
# MAGIC     0.049,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.08830,
# MAGIC
# MAGIC     0.10532,
# MAGIC
# MAGIC     0.01702,
# MAGIC
# MAGIC     ((0.10532 - 0.08830) / 0.10532) * 100,
# MAGIC
# MAGIC     'openLCA 2.6.1',
# MAGIC
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'SYNTHETIC_SCENARIO_ASSUMPTION',
# MAGIC
# MAGIC     'Screening cradle-to-gate packaging-material model. Label excluded. Bottle forming, cap molding, corrugating/converting, filling, distribution, use, and end-of-life excluded.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     modeled_packaging_mass_kg,
# MAGIC     impact_result,
# MAGIC     avoided_impact_per_unit,
# MAGIC     reduction_pct
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC WHERE scenario_id IN ('S0','S1','S2','S3')
# MAGIC ORDER BY scenario_id;