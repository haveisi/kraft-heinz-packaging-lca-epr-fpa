# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.carbon_value_parameters (
# MAGIC     carbon_value_id STRING,
# MAGIC     carbon_value_usd_per_tco2e DOUBLE,
# MAGIC     value_origin STRING,
# MAGIC     evidence_status STRING,
# MAGIC     reviewer_note STRING,
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.silver.carbon_value_parameters
# MAGIC VALUES
# MAGIC (
# MAGIC     'CV-000',
# MAGIC     0,
# MAGIC     'SYNTHETIC',
# MAGIC     'LEARNING_ASSUMPTION',
# MAGIC     'No monetary value assigned to carbon reduction.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC (
# MAGIC     'CV-050',
# MAGIC     50,
# MAGIC     'SYNTHETIC',
# MAGIC     'LEARNING_ASSUMPTION',
# MAGIC     'Illustrative internal carbon value sensitivity only.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC (
# MAGIC     'CV-100',
# MAGIC     100,
# MAGIC     'SYNTHETIC',
# MAGIC     'LEARNING_ASSUMPTION',
# MAGIC     'Illustrative internal carbon value sensitivity only.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC (
# MAGIC     'CV-150',
# MAGIC     150,
# MAGIC     'SYNTHETIC',
# MAGIC     'LEARNING_ASSUMPTION',
# MAGIC     'Illustrative internal carbon value sensitivity only.',
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_carbon_value AS
# MAGIC
# MAGIC SELECT
# MAGIC     d.scenario_id,
# MAGIC     d.scenario_name,
# MAGIC
# MAGIC     d.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     c.carbon_value_id,
# MAGIC     c.carbon_value_usd_per_tco2e,
# MAGIC
# MAGIC     d.annual_avoided_gwp_tco2e
# MAGIC         * c.carbon_value_usd_per_tco2e
# MAGIC         AS annual_carbon_value_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision d
# MAGIC
# MAGIC CROSS JOIN kraft_heinz_lca.silver.carbon_value_parameters c
# MAGIC
# MAGIC WHERE d.scenario_id IN ('S1', 'S2');

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_carbon_value
# MAGIC ORDER BY scenario_id, carbon_value_usd_per_tco2e;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_value_with_carbon AS
# MAGIC
# MAGIC SELECT
# MAGIC     d.scenario_id,
# MAGIC     d.scenario_name,
# MAGIC
# MAGIC     d.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     c.carbon_value_usd_per_tco2e,
# MAGIC     c.annual_carbon_value_usd,
# MAGIC
# MAGIC     d.annual_operating_benefit_low_usd,
# MAGIC     d.annual_operating_benefit_high_usd,
# MAGIC
# MAGIC     d.annual_operating_benefit_low_usd
# MAGIC         + c.annual_carbon_value_usd
# MAGIC         AS annual_total_value_low_usd,
# MAGIC
# MAGIC     d.annual_operating_benefit_high_usd
# MAGIC         + c.annual_carbon_value_usd
# MAGIC         AS annual_total_value_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision d
# MAGIC
# MAGIC JOIN kraft_heinz_lca.gold.v_packaging_carbon_value c
# MAGIC     ON d.scenario_id = c.scenario_id
# MAGIC
# MAGIC WHERE d.scenario_id IN ('S1','S2');

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     carbon_value_usd_per_tco2e,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_carbon_value_usd,
# MAGIC     annual_operating_benefit_low_usd,
# MAGIC     annual_operating_benefit_high_usd,
# MAGIC     annual_total_value_low_usd,
# MAGIC     annual_total_value_high_usd
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_value_with_carbon
# MAGIC ORDER BY scenario_id, carbon_value_usd_per_tco2e;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_carbon_break_even AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     annual_operating_benefit_low_usd,
# MAGIC     annual_operating_benefit_high_usd,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_avoided_gwp_tco2e > 0
# MAGIC          AND annual_operating_benefit_low_usd < 0
# MAGIC         THEN
# MAGIC             -annual_operating_benefit_low_usd
# MAGIC             / annual_avoided_gwp_tco2e
# MAGIC         ELSE 0
# MAGIC     END AS break_even_carbon_value_low_case_usd_per_tco2e,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN annual_avoided_gwp_tco2e > 0
# MAGIC          AND annual_operating_benefit_high_usd < 0
# MAGIC         THEN
# MAGIC             -annual_operating_benefit_high_usd
# MAGIC             / annual_avoided_gwp_tco2e
# MAGIC         ELSE 0
# MAGIC     END AS break_even_carbon_value_high_case_usd_per_tco2e
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_operating_decision
# MAGIC
# MAGIC WHERE scenario_id IN ('S1','S2');

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_carbon_break_even
# MAGIC ORDER BY scenario_id;