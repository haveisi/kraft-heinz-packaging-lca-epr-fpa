# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.fpa_sensitivity_parameters (
# MAGIC     parameter_set_id STRING,
# MAGIC     scenario_id STRING,
# MAGIC
# MAGIC     capex_usd DOUBLE,
# MAGIC     project_life_years INT,
# MAGIC     discount_rate DOUBLE,
# MAGIC
# MAGIC     assumption_status STRING,
# MAGIC     reviewer_note STRING,
# MAGIC
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.silver.fpa_sensitivity_parameters
# MAGIC VALUES
# MAGIC
# MAGIC -- S1 lightweighting
# MAGIC ('S1-CAPEX-25K',  'S1',  25000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp()),
# MAGIC
# MAGIC ('S1-CAPEX-50K',  'S1',  50000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp()),
# MAGIC
# MAGIC ('S1-CAPEX-100K', 'S1', 100000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp()),
# MAGIC
# MAGIC -- S2 rPET
# MAGIC ('S2-CAPEX-25K',  'S2',  25000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp()),
# MAGIC
# MAGIC ('S2-CAPEX-50K',  'S2',  50000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp()),
# MAGIC
# MAGIC ('S2-CAPEX-100K', 'S2', 100000, 5, 0.10, 'SYNTHETIC_LEARNING_ASSUMPTION',
# MAGIC  'Illustrative CAPEX only; not Kraft Heinz reported data.', current_timestamp());

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_npv_sensitivity AS
# MAGIC
# MAGIC WITH base AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         scenario_id,
# MAGIC         scenario_name,
# MAGIC
# MAGIC         annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC         annual_operating_benefit_low_usd,
# MAGIC         annual_operating_benefit_high_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_packaging_operating_decision
# MAGIC
# MAGIC     WHERE scenario_id IN ('S1','S2')
# MAGIC ),
# MAGIC
# MAGIC x AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         b.*,
# MAGIC
# MAGIC         p.parameter_set_id,
# MAGIC         p.capex_usd,
# MAGIC         p.project_life_years,
# MAGIC         p.discount_rate,
# MAGIC         p.assumption_status
# MAGIC
# MAGIC     FROM base b
# MAGIC
# MAGIC     INNER JOIN kraft_heinz_lca.silver.fpa_sensitivity_parameters p
# MAGIC         ON b.scenario_id = p.scenario_id
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     -capex_usd
# MAGIC     +
# MAGIC     annual_operating_benefit_low_usd
# MAGIC     *
# MAGIC     (
# MAGIC         (1 - POWER(1 + discount_rate, -project_life_years))
# MAGIC         / discount_rate
# MAGIC     )
# MAGIC         AS npv_low_case_usd,
# MAGIC
# MAGIC     -capex_usd
# MAGIC     +
# MAGIC     annual_operating_benefit_high_usd
# MAGIC     *
# MAGIC     (
# MAGIC         (1 - POWER(1 + discount_rate, -project_life_years))
# MAGIC         / discount_rate
# MAGIC     )
# MAGIC         AS npv_high_case_usd,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_operating_benefit_low_usd > 0
# MAGIC         THEN capex_usd / annual_operating_benefit_low_usd
# MAGIC     END AS simple_payback_low_case_years,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_operating_benefit_high_usd > 0
# MAGIC         THEN capex_usd / annual_operating_benefit_high_usd
# MAGIC     END AS simple_payback_high_case_years
# MAGIC
# MAGIC FROM x;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     parameter_set_id,
# MAGIC     capex_usd,
# MAGIC
# MAGIC     annual_operating_benefit_low_usd,
# MAGIC     annual_operating_benefit_high_usd,
# MAGIC
# MAGIC     npv_low_case_usd,
# MAGIC     npv_high_case_usd,
# MAGIC
# MAGIC     simple_payback_low_case_years,
# MAGIC     simple_payback_high_case_years
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_npv_sensitivity
# MAGIC
# MAGIC ORDER BY scenario_id, capex_usd;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_break_even_capex AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     annual_operating_benefit_low_usd,
# MAGIC     annual_operating_benefit_high_usd,
# MAGIC
# MAGIC     5 AS project_life_years,
# MAGIC     0.10 AS discount_rate,
# MAGIC
# MAGIC     annual_operating_benefit_low_usd
# MAGIC     *
# MAGIC     ((1 - POWER(1.10, -5)) / 0.10)
# MAGIC         AS max_capex_for_zero_npv_low_case_usd,
# MAGIC
# MAGIC     annual_operating_benefit_high_usd
# MAGIC     *
# MAGIC     ((1 - POWER(1.10, -5)) / 0.10)
# MAGIC         AS max_capex_for_zero_npv_high_case_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision
# MAGIC
# MAGIC WHERE scenario_id IN ('S1','S2');

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_break_even_capex;