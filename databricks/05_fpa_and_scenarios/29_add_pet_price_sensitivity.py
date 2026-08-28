# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.silver.financial_assumption_registry
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'FIN-VPET-2026-MID',
# MAGIC     'ALL',
# MAGIC     'Virgin PET market proxy',
# MAGIC     1.156,
# MAGIC     'USD/kg',
# MAGIC     'EXTERNAL_MARKET_PROXY',
# MAGIC     'VERIFIED_PUBLIC_MARKET_REFERENCE',
# MAGIC     'IMARC PET Resin Prices Q2 2026 USA',
# MAGIC     NULL,
# MAGIC     DATE '2026-06-30',
# MAGIC     'USA Q2 2026 PET resin reference. Not a Kraft Heinz contract price.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-RPET-2026-LOW',
# MAGIC     'S2',
# MAGIC     'rPET market proxy - low',
# MAGIC     1.650,
# MAGIC     'USD/kg',
# MAGIC     'EXTERNAL_MARKET_PROXY',
# MAGIC     'VERIFIED_PUBLIC_MARKET_REFERENCE',
# MAGIC     'Procurement Resource Recycled PET USA June 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-06-30',
# MAGIC     'USA recycled PET EXW reference. Use as lower sensitivity case, not Kraft Heinz purchasing data.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-RPET-2026-HIGH',
# MAGIC     'S2',
# MAGIC     'rPET food-grade pellet proxy - high',
# MAGIC     1.808,
# MAGIC     'USD/kg',
# MAGIC     'EXTERNAL_MARKET_PROXY',
# MAGIC     'VERIFIED_PUBLIC_MARKET_REFERENCE',
# MAGIC     'North America food-grade rPET pellet August 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-08-01',
# MAGIC     'Food-grade pellet market proxy. Use as upper sensitivity case.',
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_pet_procurement_sensitivity AS
# MAGIC
# MAGIC WITH prices AS (
# MAGIC     SELECT
# MAGIC         MAX(CASE
# MAGIC             WHEN assumption_id = 'FIN-VPET-2026-MID'
# MAGIC             THEN value END) AS vpet_usd_per_kg,
# MAGIC
# MAGIC         MAX(CASE
# MAGIC             WHEN assumption_id = 'FIN-RPET-2026-LOW'
# MAGIC             THEN value END) AS rpet_low_usd_per_kg,
# MAGIC
# MAGIC         MAX(CASE
# MAGIC             WHEN assumption_id = 'FIN-RPET-2026-HIGH'
# MAGIC             THEN value END) AS rpet_high_usd_per_kg
# MAGIC
# MAGIC     FROM kraft_heinz_lca.silver.financial_assumption_registry
# MAGIC ),
# MAGIC
# MAGIC scenarios AS (
# MAGIC     SELECT *
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_delta
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     s.scenario_id,
# MAGIC     s.scenario_name,
# MAGIC
# MAGIC     p.vpet_usd_per_kg,
# MAGIC     p.rpet_low_usd_per_kg,
# MAGIC     p.rpet_high_usd_per_kg,
# MAGIC
# MAGIC     s.annual_total_pet_bottle_kg,
# MAGIC     s.annual_virgin_pet_kg,
# MAGIC     s.annual_rpet_kg,
# MAGIC
# MAGIC     /* Baseline equivalent PET cost */
# MAGIC     150000 * p.vpet_usd_per_kg
# MAGIC         AS baseline_pet_cost_usd,
# MAGIC
# MAGIC     /* Scenario material cost - lower rPET case */
# MAGIC     s.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + s.annual_rpet_kg * p.rpet_low_usd_per_kg
# MAGIC         AS scenario_material_cost_low_usd,
# MAGIC
# MAGIC     /* Scenario material cost - higher rPET case */
# MAGIC     s.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + s.annual_rpet_kg * p.rpet_high_usd_per_kg
# MAGIC         AS scenario_material_cost_high_usd
# MAGIC
# MAGIC FROM scenarios s
# MAGIC CROSS JOIN prices p;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     baseline_pet_cost_usd,
# MAGIC
# MAGIC     scenario_material_cost_low_usd,
# MAGIC     scenario_material_cost_high_usd,
# MAGIC
# MAGIC     baseline_pet_cost_usd
# MAGIC       - scenario_material_cost_low_usd
# MAGIC         AS material_savings_low_usd,
# MAGIC
# MAGIC     baseline_pet_cost_usd
# MAGIC       - scenario_material_cost_high_usd
# MAGIC         AS material_savings_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_sensitivity
# MAGIC ORDER BY scenario_id;