# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.ca_sb54_fee_registry (
# MAGIC     fee_id STRING,
# MAGIC
# MAGIC     jurisdiction STRING,
# MAGIC     program_name STRING,
# MAGIC
# MAGIC     fee_year INT,
# MAGIC
# MAGIC     cmc_id STRING,
# MAGIC     material_class STRING,
# MAGIC     material_type STRING,
# MAGIC     form STRING,
# MAGIC
# MAGIC     base_fee_usd_per_kg DOUBLE,
# MAGIC     eco_modulation_factor DOUBLE,
# MAGIC     effective_fee_usd_per_kg DOUBLE,
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
# MAGIC INSERT INTO kraft_heinz_lca.silver.ca_sb54_fee_registry
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'CA-SB54-PET-P2P-2027',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC
# MAGIC     '25_P2P',
# MAGIC     'Plastic',
# MAGIC     'PET (#1)',
# MAGIC     'Bottles, Jugs, and Jars (Pigmented/Color)',
# MAGIC
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'PENDING_VERIFIED_FEE',
# MAGIC
# MAGIC     'CalRecycle / CAA current program materials',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'REGULATORY_PENDING_FEE',
# MAGIC
# MAGIC     'CMC is established, but no verified final fee value has yet been loaded into this project.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA-SB54-PP-CAP-2027',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC
# MAGIC     NULL,
# MAGIC     'Plastic',
# MAGIC     'PP (#5)',
# MAGIC     'Closure / cap',
# MAGIC
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'PENDING_FINAL_CMC_AND_FEE',
# MAGIC
# MAGIC     'CalRecycle / CAA current program materials',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'REGULATORY_PENDING_FEE',
# MAGIC
# MAGIC     'Cap material is PP, but final CMC remains provisional between general PP lid and small-format classification.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA-SB54-CORR-2027',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC
# MAGIC     NULL,
# MAGIC     'Paper and Fiber',
# MAGIC     'Corrugated board',
# MAGIC     'Shipping case allocation',
# MAGIC
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'PENDING_FINAL_CMC_AND_FEE',
# MAGIC
# MAGIC     'CalRecycle / CAA current program materials',
# MAGIC     NULL,
# MAGIC     NULL,
# MAGIC
# MAGIC     'REGULATORY_PENDING_FEE',
# MAGIC
# MAGIC     'Corrugated material is modeled, but plastic-component status and final CMC are not yet verified.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     fee_id,
# MAGIC     cmc_id,
# MAGIC     material_type,
# MAGIC     base_fee_usd_per_kg,
# MAGIC     fee_status,
# MAGIC     data_classification
# MAGIC FROM kraft_heinz_lca.silver.ca_sb54_fee_registry;