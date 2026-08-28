# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_illustrative_epr_cost_all AS
# MAGIC
# MAGIC WITH x AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC         scenario_name,
# MAGIC         annual_units_sold,
# MAGIC
# MAGIC         annual_total_pet_bottle_kg,
# MAGIC         annual_pp_cap_kg,
# MAGIC         annual_containerboard_kg,
# MAGIC
# MAGIC         annual_total_pet_bottle_kg * 2.2046226218 AS pet_lb,
# MAGIC         annual_pp_cap_kg * 2.2046226218 AS pp_lb,
# MAGIC         annual_containerboard_kg * 2.2046226218 AS corrugated_lb
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     annual_units_sold,
# MAGIC
# MAGIC     annual_total_pet_bottle_kg,
# MAGIC     annual_pp_cap_kg,
# MAGIC     annual_containerboard_kg,
# MAGIC
# MAGIC     /* LOW CAA ILLUSTRATIVE CASE */
# MAGIC
# MAGIC     pet_lb * (0.13 + 0.04 + 0.17)
# MAGIC         + annual_units_sold * 0.001
# MAGIC         AS pet_fee_low_usd,
# MAGIC
# MAGIC     pp_lb * (0.11 + 0.04 + 0.17)
# MAGIC         + annual_units_sold * 0.001
# MAGIC         AS pp_cap_fee_low_usd,
# MAGIC
# MAGIC     corrugated_lb * 0.02
# MAGIC         AS corrugated_fee_low_usd,
# MAGIC
# MAGIC     /* HIGH CAA ILLUSTRATIVE CASE */
# MAGIC
# MAGIC     pet_lb * (0.38 + 0.10 + 0.25)
# MAGIC         + annual_units_sold * 0.0012
# MAGIC         AS pet_fee_high_usd,
# MAGIC
# MAGIC     pp_lb * (0.24 + 0.10 + 0.25)
# MAGIC         + annual_units_sold * 0.0012
# MAGIC         AS pp_cap_fee_high_usd,
# MAGIC
# MAGIC     corrugated_lb * 0.05
# MAGIC         AS corrugated_fee_high_usd
# MAGIC
# MAGIC FROM x;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_cost_summary_all AS
# MAGIC
# MAGIC WITH costs AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         *,
# MAGIC
# MAGIC         pet_fee_low_usd
# MAGIC           + pp_cap_fee_low_usd
# MAGIC           + corrugated_fee_low_usd
# MAGIC             AS total_epr_low_usd,
# MAGIC
# MAGIC         pet_fee_high_usd
# MAGIC           + pp_cap_fee_high_usd
# MAGIC           + corrugated_fee_high_usd
# MAGIC             AS total_epr_high_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_illustrative_epr_cost_all
# MAGIC ),
# MAGIC
# MAGIC baseline AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         total_epr_low_usd  AS baseline_low_usd,
# MAGIC         total_epr_high_usd AS baseline_high_usd
# MAGIC
# MAGIC     FROM costs
# MAGIC     WHERE scenario_id = 'S0'
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     c.*,
# MAGIC
# MAGIC     b.baseline_low_usd - c.total_epr_low_usd
# MAGIC         AS annual_epr_savings_low_usd,
# MAGIC
# MAGIC     b.baseline_high_usd - c.total_epr_high_usd
# MAGIC         AS annual_epr_savings_high_usd
# MAGIC
# MAGIC FROM costs c
# MAGIC CROSS JOIN baseline b;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     total_epr_low_usd,
# MAGIC     total_epr_high_usd,
# MAGIC     annual_epr_savings_low_usd,
# MAGIC     annual_epr_savings_high_usd
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC ORDER BY scenario_id;