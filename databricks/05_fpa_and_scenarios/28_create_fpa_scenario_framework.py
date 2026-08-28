# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.financial_assumption_registry (
# MAGIC
# MAGIC     assumption_id STRING,
# MAGIC
# MAGIC     scenario_id STRING,
# MAGIC     cost_driver STRING,
# MAGIC
# MAGIC     value DOUBLE,
# MAGIC     unit STRING,
# MAGIC
# MAGIC     value_origin STRING,
# MAGIC     evidence_status STRING,
# MAGIC
# MAGIC     source_name STRING,
# MAGIC     source_url STRING,
# MAGIC     source_date DATE,
# MAGIC
# MAGIC     reviewer_note STRING,
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.silver.financial_assumption_registry
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'FIN-S1-CAPEX',
# MAGIC     'S1',
# MAGIC     'Implementation CAPEX',
# MAGIC     NULL,
# MAGIC     'USD',
# MAGIC     'UNKNOWN',
# MAGIC     'REQUIRES_EVIDENCE',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     'Bottle lightweighting may require tooling, engineering validation, line trials, quality testing, and supplier qualification. No SKU-specific Kraft Heinz CAPEX has been identified.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-S1-VPET-PRICE',
# MAGIC     'S1',
# MAGIC     'Virgin PET purchase price',
# MAGIC     NULL,
# MAGIC     'USD/kg',
# MAGIC     'UNKNOWN',
# MAGIC     'REQUIRES_EVIDENCE',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     'Required to monetize the 3 g PET reduction per package. Do not substitute a generic resin price without documenting source geography and period.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-S2-CAPEX',
# MAGIC     'S2',
# MAGIC     'Implementation CAPEX',
# MAGIC     NULL,
# MAGIC     'USD',
# MAGIC     'UNKNOWN',
# MAGIC     'REQUIRES_EVIDENCE',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     'Potential qualification, testing, tooling, procurement and processing costs for 30% rPET are not yet known.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-S2-VPET-PRICE',
# MAGIC     'S2',
# MAGIC     'Virgin PET purchase price',
# MAGIC     NULL,
# MAGIC     'USD/kg',
# MAGIC     'UNKNOWN',
# MAGIC     'REQUIRES_EVIDENCE',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     'Needed to calculate avoided virgin PET procurement cost.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'FIN-S2-RPET-PRICE',
# MAGIC     'S2',
# MAGIC     'Recycled PET purchase price',
# MAGIC     NULL,
# MAGIC     'USD/kg',
# MAGIC     'UNKNOWN',
# MAGIC     'REQUIRES_EVIDENCE',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     'Needed to calculate the cost or premium associated with replacing 9 g virgin PET with rPET.',
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_scenario_epr_savings AS
# MAGIC
# MAGIC WITH x AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC         scenario_name,
# MAGIC         total_epr_low_usd,
# MAGIC         total_epr_high_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_cost_summary
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC baseline AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         total_epr_low_usd  AS baseline_low_usd,
# MAGIC         total_epr_high_usd AS baseline_high_usd
# MAGIC
# MAGIC     FROM x
# MAGIC     WHERE scenario_id = 'S0'
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     x.scenario_id,
# MAGIC     x.scenario_name,
# MAGIC
# MAGIC     x.total_epr_low_usd,
# MAGIC     x.total_epr_high_usd,
# MAGIC
# MAGIC     b.baseline_low_usd
# MAGIC         - x.total_epr_low_usd
# MAGIC         AS annual_epr_savings_low_usd,
# MAGIC
# MAGIC     b.baseline_high_usd
# MAGIC         - x.total_epr_high_usd
# MAGIC         AS annual_epr_savings_high_usd
# MAGIC
# MAGIC FROM x
# MAGIC CROSS JOIN baseline b;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_scenario_epr_savings
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_fpa_bridge AS
# MAGIC
# MAGIC SELECT
# MAGIC     l.scenario_id,
# MAGIC     l.scenario_name,
# MAGIC
# MAGIC     l.modeled_packaging_mass_kg,
# MAGIC
# MAGIC     l.gwp_kg_co2e_per_package,
# MAGIC     l.avoided_gwp_kg_co2e_per_package,
# MAGIC     l.reduction_pct AS gwp_reduction_pct,
# MAGIC
# MAGIC     ca.annual_units_sold,
# MAGIC     ca.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     e.annual_epr_savings_low_usd,
# MAGIC     e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN l.scenario_id = 'S0' THEN 0
# MAGIC         WHEN l.scenario_id = 'S1' THEN 15000
# MAGIC         WHEN l.scenario_id = 'S2' THEN 45000
# MAGIC     END AS annual_virgin_pet_reduction_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN l.scenario_id = 'S2' THEN 45000
# MAGIC         ELSE 0
# MAGIC     END AS annual_rpet_requirement_kg,
# MAGIC
# MAGIC     CAST(NULL AS DOUBLE) AS annual_material_cost_change_usd,
# MAGIC
# MAGIC     CAST(NULL AS DOUBLE) AS implementation_capex_usd,
# MAGIC
# MAGIC     CAST(NULL AS DOUBLE) AS annual_net_cash_benefit_usd,
# MAGIC
# MAGIC     CAST(NULL AS DOUBLE) AS simple_payback_years
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_lca_scenario_comparison l
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_lca_scenario_california ca
# MAGIC     ON l.scenario_id = ca.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_scenario_epr_savings e
# MAGIC     ON l.scenario_id = e.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_fpa_bridge
# MAGIC ORDER BY scenario_id;