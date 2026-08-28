# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_pet_procurement_all_scenarios AS
# MAGIC
# MAGIC WITH prices AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-VPET-2026-MID'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS vpet_usd_per_kg,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-RPET-2026-LOW'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS rpet_low_usd_per_kg,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-RPET-2026-HIGH'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS rpet_high_usd_per_kg
# MAGIC
# MAGIC     FROM kraft_heinz_lca.silver.financial_assumption_registry
# MAGIC ),
# MAGIC
# MAGIC x AS (
# MAGIC
# MAGIC     SELECT *
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     x.scenario_id,
# MAGIC     x.scenario_name,
# MAGIC
# MAGIC     x.annual_virgin_pet_kg,
# MAGIC     x.annual_rpet_kg,
# MAGIC
# MAGIC     p.vpet_usd_per_kg,
# MAGIC     p.rpet_low_usd_per_kg,
# MAGIC     p.rpet_high_usd_per_kg,
# MAGIC
# MAGIC     150000 * p.vpet_usd_per_kg
# MAGIC         AS baseline_pet_cost_usd,
# MAGIC
# MAGIC     x.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + x.annual_rpet_kg * p.rpet_low_usd_per_kg
# MAGIC         AS scenario_pet_cost_low_usd,
# MAGIC
# MAGIC     x.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + x.annual_rpet_kg * p.rpet_high_usd_per_kg
# MAGIC         AS scenario_pet_cost_high_usd
# MAGIC
# MAGIC FROM x
# MAGIC CROSS JOIN prices p;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_pet_procurement_savings_all AS
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     baseline_pet_cost_usd
# MAGIC       - scenario_pet_cost_low_usd
# MAGIC         AS material_savings_low_usd,
# MAGIC
# MAGIC     baseline_pet_cost_usd
# MAGIC       - scenario_pet_cost_high_usd
# MAGIC         AS material_savings_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_all_scenarios;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_integrated_operating_case AS
# MAGIC
# MAGIC SELECT
# MAGIC     s.scenario_id,
# MAGIC     s.scenario_name,
# MAGIC
# MAGIC     s.gwp_kg_co2e_per_package,
# MAGIC     s.gwp_reduction_pct,
# MAGIC     s.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     s.annual_plastic_source_reduction_kg,
# MAGIC     s.annual_virgin_pet_displacement_kg,
# MAGIC     s.annual_rpet_kg,
# MAGIC
# MAGIC     p.material_savings_low_usd,
# MAGIC     p.material_savings_high_usd,
# MAGIC
# MAGIC     e.annual_epr_savings_low_usd,
# MAGIC     e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC     p.material_savings_low_usd
# MAGIC       + e.annual_epr_savings_low_usd
# MAGIC         AS annual_operating_value_low_case_usd,
# MAGIC
# MAGIC     p.material_savings_high_usd
# MAGIC       + e.annual_epr_savings_high_usd
# MAGIC         AS annual_operating_value_high_case_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master s
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_pet_procurement_savings_all p
# MAGIC     ON s.scenario_id = p.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_cost_summary_all e
# MAGIC     ON s.scenario_id = e.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     material_savings_low_usd,
# MAGIC     material_savings_high_usd,
# MAGIC
# MAGIC     annual_epr_savings_low_usd,
# MAGIC     annual_epr_savings_high_usd,
# MAGIC
# MAGIC     annual_operating_value_low_case_usd,
# MAGIC     annual_operating_value_high_case_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_integrated_operating_case
# MAGIC
# MAGIC ORDER BY scenario_id;