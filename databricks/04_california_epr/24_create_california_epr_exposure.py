# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_scenario_basis AS
# MAGIC
# MAGIC SELECT
# MAGIC     s.scenario_id,
# MAGIC     s.scenario_name,
# MAGIC
# MAGIC     mv.jurisdiction,
# MAGIC     mv.reporting_year,
# MAGIC     mv.annual_units_sold,
# MAGIC
# MAGIC     /* Bottle composition */
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.021
# MAGIC     END AS virgin_pet_kg_per_unit,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id IN ('S0','S1') THEN 0.000
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.009
# MAGIC     END AS rpet_kg_per_unit,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.030
# MAGIC     END AS total_pet_bottle_kg_per_unit,
# MAGIC
# MAGIC     /* Other modeled packaging */
# MAGIC     0.004 AS pp_cap_kg_per_unit,
# MAGIC     0.018 AS containerboard_kg_per_unit,
# MAGIC
# MAGIC     /* Annual placed-on-market masses */
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.021 * mv.annual_units_sold
# MAGIC     END AS annual_virgin_pet_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id IN ('S0','S1') THEN 0
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.009 * mv.annual_units_sold
# MAGIC     END AS annual_rpet_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN s.scenario_id = 'S0' THEN 0.030 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S1' THEN 0.027 * mv.annual_units_sold
# MAGIC         WHEN s.scenario_id = 'S2' THEN 0.030 * mv.annual_units_sold
# MAGIC     END AS annual_total_pet_bottle_kg,
# MAGIC
# MAGIC     0.004 * mv.annual_units_sold AS annual_pp_cap_kg,
# MAGIC
# MAGIC     0.018 * mv.annual_units_sold AS annual_containerboard_kg,
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
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_scenario_delta AS
# MAGIC
# MAGIC WITH x AS (
# MAGIC     SELECT *
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis
# MAGIC ),
# MAGIC
# MAGIC baseline AS (
# MAGIC     SELECT
# MAGIC         annual_total_pet_bottle_kg AS baseline_pet_kg,
# MAGIC         annual_virgin_pet_kg AS baseline_virgin_pet_kg
# MAGIC     FROM x
# MAGIC     WHERE scenario_id = 'S0'
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     x.scenario_id,
# MAGIC     x.scenario_name,
# MAGIC
# MAGIC     x.annual_total_pet_bottle_kg,
# MAGIC     x.annual_virgin_pet_kg,
# MAGIC     x.annual_rpet_kg,
# MAGIC
# MAGIC     b.baseline_pet_kg
# MAGIC         - x.annual_total_pet_bottle_kg
# MAGIC         AS annual_plastic_source_reduction_kg,
# MAGIC
# MAGIC     b.baseline_virgin_pet_kg
# MAGIC         - x.annual_virgin_pet_kg
# MAGIC         AS annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN x.scenario_id = 'S0'
# MAGIC             THEN 'BASELINE'
# MAGIC
# MAGIC         WHEN b.baseline_pet_kg
# MAGIC              - x.annual_total_pet_bottle_kg > 0
# MAGIC             THEN 'SOURCE_REDUCTION'
# MAGIC
# MAGIC         WHEN x.annual_rpet_kg > 0
# MAGIC             THEN 'RECYCLED_CONTENT'
# MAGIC
# MAGIC         ELSE 'OTHER'
# MAGIC     END AS sb54_strategy_type
# MAGIC
# MAGIC FROM x
# MAGIC CROSS JOIN baseline b;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_delta
# MAGIC ORDER BY scenario_id;