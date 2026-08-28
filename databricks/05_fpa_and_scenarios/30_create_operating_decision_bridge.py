# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_operating_decision AS
# MAGIC
# MAGIC WITH procurement AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC         scenario_name,
# MAGIC
# MAGIC         baseline_pet_cost_usd,
# MAGIC         scenario_material_cost_low_usd,
# MAGIC         scenario_material_cost_high_usd,
# MAGIC
# MAGIC         baseline_pet_cost_usd
# MAGIC           - scenario_material_cost_low_usd
# MAGIC             AS material_savings_case_a_usd,
# MAGIC
# MAGIC         baseline_pet_cost_usd
# MAGIC           - scenario_material_cost_high_usd
# MAGIC             AS material_savings_case_b_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_pet_procurement_sensitivity
# MAGIC ),
# MAGIC
# MAGIC epr AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC
# MAGIC         annual_epr_savings_low_usd,
# MAGIC         annual_epr_savings_high_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_scenario_epr_savings
# MAGIC ),
# MAGIC
# MAGIC carbon AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC         scenario_name,
# MAGIC
# MAGIC         annual_avoided_gwp_tco2e
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_lca_scenario_california
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     p.scenario_id,
# MAGIC     p.scenario_name,
# MAGIC
# MAGIC     c.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     p.material_savings_case_a_usd,
# MAGIC     p.material_savings_case_b_usd,
# MAGIC
# MAGIC     e.annual_epr_savings_low_usd,
# MAGIC     e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC     /* Conservative annual operating benefit */
# MAGIC     LEAST(
# MAGIC         p.material_savings_case_a_usd,
# MAGIC         p.material_savings_case_b_usd
# MAGIC     )
# MAGIC     +
# MAGIC     LEAST(
# MAGIC         e.annual_epr_savings_low_usd,
# MAGIC         e.annual_epr_savings_high_usd
# MAGIC     )
# MAGIC         AS annual_operating_benefit_low_usd,
# MAGIC
# MAGIC     /* More favorable annual operating benefit */
# MAGIC     GREATEST(
# MAGIC         p.material_savings_case_a_usd,
# MAGIC         p.material_savings_case_b_usd
# MAGIC     )
# MAGIC     +
# MAGIC     GREATEST(
# MAGIC         e.annual_epr_savings_low_usd,
# MAGIC         e.annual_epr_savings_high_usd
# MAGIC     )
# MAGIC         AS annual_operating_benefit_high_usd
# MAGIC
# MAGIC FROM procurement p
# MAGIC
# MAGIC LEFT JOIN epr e
# MAGIC     ON p.scenario_id = e.scenario_id
# MAGIC
# MAGIC LEFT JOIN carbon c
# MAGIC     ON p.scenario_id = c.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_abatement_economics AS
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_avoided_gwp_tco2e > 0
# MAGIC         THEN
# MAGIC             -annual_operating_benefit_low_usd
# MAGIC             / annual_avoided_gwp_tco2e
# MAGIC     END AS operating_cost_per_tco2e_low_case,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_avoided_gwp_tco2e > 0
# MAGIC         THEN
# MAGIC             -annual_operating_benefit_high_usd
# MAGIC             / annual_avoided_gwp_tco2e
# MAGIC     END AS operating_cost_per_tco2e_high_case
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_operating_benefit_low_usd,
# MAGIC     annual_operating_benefit_high_usd,
# MAGIC     operating_cost_per_tco2e_low_case,
# MAGIC     operating_cost_per_tco2e_high_case
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_abatement_economics
# MAGIC ORDER BY scenario_id;