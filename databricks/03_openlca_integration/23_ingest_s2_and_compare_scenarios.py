# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.lca_scenario_summary (
# MAGIC     scenario_result_id STRING,
# MAGIC
# MAGIC     model_id STRING,
# MAGIC     sku_id STRING,
# MAGIC
# MAGIC     scenario_id STRING,
# MAGIC     scenario_name STRING,
# MAGIC
# MAGIC     functional_unit STRING,
# MAGIC
# MAGIC     modeled_packaging_mass_kg DOUBLE,
# MAGIC
# MAGIC     impact_method STRING,
# MAGIC     impact_category STRING,
# MAGIC     impact_unit STRING,
# MAGIC
# MAGIC     impact_result DOUBLE,
# MAGIC
# MAGIC     baseline_impact_result DOUBLE,
# MAGIC     avoided_impact_per_unit DOUBLE,
# MAGIC     reduction_pct DOUBLE,
# MAGIC
# MAGIC     result_source STRING,
# MAGIC     result_status STRING,
# MAGIC
# MAGIC     data_classification STRING,
# MAGIC     limitation_note STRING,
# MAGIC
# MAGIC     calculated_at TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SHOW TABLES IN kraft_heinz_lca.gold;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC VALUES (
# MAGIC     'LCA-S1-GWP-SUMMARY',
# MAGIC
# MAGIC     'OLCA-KH-S1-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC
# MAGIC     0.049,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.09887,
# MAGIC
# MAGIC     0.10532,
# MAGIC
# MAGIC     0.10532 - 0.09887,
# MAGIC
# MAGIC     ((0.10532 - 0.09887) / 0.10532) * 100,
# MAGIC
# MAGIC     'openLCA 2.6.1',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'SYNTHETIC_SCENARIO_ASSUMPTION',
# MAGIC
# MAGIC     '10% PET lightweighting is a learning scenario, not a reported Kraft Heinz redesign. Label, converting, filling, distribution and end-of-life remain outside the screening boundary.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC VALUES (
# MAGIC     'LCA-S2-GWP-SUMMARY',
# MAGIC
# MAGIC     'OLCA-KH-S2-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC
# MAGIC     'S2',
# MAGIC     'PET Bottle 30% rPET',
# MAGIC
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC
# MAGIC     0.052,
# MAGIC
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC
# MAGIC     0.09357,
# MAGIC
# MAGIC     0.10532,
# MAGIC
# MAGIC     0.10532 - 0.09357,
# MAGIC
# MAGIC     ((0.10532 - 0.09357) / 0.10532) * 100,
# MAGIC
# MAGIC     'openLCA 2.6.1',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC
# MAGIC     'SYNTHETIC_SCENARIO_ASSUMPTION',
# MAGIC
# MAGIC     '30% rPET learning scenario. rPET pellet process comes from Federal LCA Commons/USLCI with linked upstream providers. Scenario percentage is not reported for this Heinz SKU.',
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
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_lca_scenario_comparison AS
# MAGIC
# MAGIC SELECT
# MAGIC     'S0' AS scenario_id,
# MAGIC     'Baseline' AS scenario_name,
# MAGIC     0.052 AS modeled_packaging_mass_kg,
# MAGIC     0.10532 AS gwp_kg_co2e_per_package,
# MAGIC     0.0 AS avoided_gwp_kg_co2e_per_package,
# MAGIC     0.0 AS reduction_pct
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     modeled_packaging_mass_kg,
# MAGIC     impact_result AS gwp_kg_co2e_per_package,
# MAGIC     avoided_impact_per_unit AS avoided_gwp_kg_co2e_per_package,
# MAGIC     reduction_pct
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_lca_scenario_comparison
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_lca_scenario_california AS
# MAGIC
# MAGIC SELECT
# MAGIC     s.scenario_id,
# MAGIC     s.scenario_name,
# MAGIC
# MAGIC     mv.jurisdiction,
# MAGIC     mv.reporting_year,
# MAGIC     mv.annual_units_sold,
# MAGIC
# MAGIC     s.modeled_packaging_mass_kg,
# MAGIC     s.gwp_kg_co2e_per_package,
# MAGIC     s.avoided_gwp_kg_co2e_per_package,
# MAGIC     s.reduction_pct,
# MAGIC
# MAGIC     s.gwp_kg_co2e_per_package
# MAGIC         * mv.annual_units_sold
# MAGIC         / 1000.0
# MAGIC         AS annual_gwp_tco2e,
# MAGIC
# MAGIC     s.avoided_gwp_kg_co2e_per_package
# MAGIC         * mv.annual_units_sold
# MAGIC         / 1000.0
# MAGIC         AS annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     mv.data_classification AS market_volume_status
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_lca_scenario_comparison s
# MAGIC CROSS JOIN kraft_heinz_lca.gold.market_volume mv
# MAGIC
# MAGIC WHERE mv.sku_id = 'SKU-KH-20OZ'
# MAGIC   AND mv.jurisdiction = 'California';

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_lca_scenario_california
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_material_scenario AS
# MAGIC
# MAGIC SELECT
# MAGIC     s.scenario_id,
# MAGIC     s.scenario_name,
# MAGIC
# MAGIC     mv.annual_units_sold,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.021
# MAGIC     END AS virgin_pet_kg_per_package,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id IN ('S0','S1') THEN 0.000
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.009
# MAGIC     END AS rpet_kg_per_package,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.030
# MAGIC     END AS total_bottle_pet_kg_per_package,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.021 * mv.annual_units_sold
# MAGIC     END AS annual_virgin_pet_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id IN ('S0','S1') THEN 0
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.009 * mv.annual_units_sold
# MAGIC     END AS annual_rpet_kg
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_lca_scenario_comparison s
# MAGIC CROSS JOIN kraft_heinz_lca.gold.market_volume mv
# MAGIC
# MAGIC WHERE mv.sku_id = 'SKU-KH-20OZ'
# MAGIC   AND mv.jurisdiction = 'California';

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_material_scenario
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

