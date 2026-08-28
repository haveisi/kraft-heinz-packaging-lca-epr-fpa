# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.ca_sb54_illustrative_fee_model (
# MAGIC     illustrative_fee_id STRING,
# MAGIC
# MAGIC     jurisdiction STRING,
# MAGIC     program_name STRING,
# MAGIC
# MAGIC     fee_year INT,
# MAGIC
# MAGIC     cmc_id STRING,
# MAGIC     material_type STRING,
# MAGIC     form STRING,
# MAGIC
# MAGIC     illustrative_fee_usd_per_kg DOUBLE,
# MAGIC
# MAGIC     fee_status STRING,
# MAGIC     source_name STRING,
# MAGIC     source_url STRING,
# MAGIC     source_date DATE,
# MAGIC
# MAGIC     data_classification STRING,
# MAGIC     reviewer_note STRING,
# MAGIC
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_cost_ready AS
# MAGIC
# MAGIC SELECT
# MAGIC     e.scenario_id,
# MAGIC     e.scenario_name,
# MAGIC
# MAGIC     e.annual_total_pet_bottle_kg,
# MAGIC     e.annual_virgin_pet_kg,
# MAGIC     e.annual_rpet_kg,
# MAGIC
# MAGIC     e.annual_plastic_source_reduction_kg,
# MAGIC     e.annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     f.cmc_id,
# MAGIC     f.illustrative_fee_usd_per_kg,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN f.illustrative_fee_usd_per_kg IS NULL
# MAGIC         THEN NULL
# MAGIC
# MAGIC         ELSE
# MAGIC             e.annual_total_pet_bottle_kg
# MAGIC             * f.illustrative_fee_usd_per_kg
# MAGIC     END AS illustrative_pet_epr_cost_usd,
# MAGIC
# MAGIC     f.fee_status,
# MAGIC     f.data_classification
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_delta e
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.silver.ca_sb54_illustrative_fee_model f
# MAGIC     ON f.cmc_id = '25_P2P'
# MAGIC    AND f.fee_year = 2027;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_ready
# MAGIC ORDER BY scenario_id;