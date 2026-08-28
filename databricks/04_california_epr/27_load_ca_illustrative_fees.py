# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.silver.ca_sb54_illustrative_fee_model
# MAGIC VALUES
# MAGIC
# MAGIC (
# MAGIC     'CA2027-LOW-PET-P2P',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_P2P',
# MAGIC     'PET (#1)',
# MAGIC     'Bottles, Jugs, and Jars (Pigmented/Color)',
# MAGIC     0.13,
# MAGIC     'ILLUSTRATIVE_LOW',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Total Base Fee only. Reuse Investment, PPMF weight-based, and PPMF component-based fees are stored separately in the calculation layer.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA2027-HIGH-PET-P2P',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_P2P',
# MAGIC     'PET (#1)',
# MAGIC     'Bottles, Jugs, and Jars (Pigmented/Color)',
# MAGIC     0.38,
# MAGIC     'ILLUSTRATIVE_HIGH',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Total Base Fee only.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA2027-LOW-PP-P41P',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_P41P',
# MAGIC     'PP (#5)',
# MAGIC     'Other Rigid Containers, Cups, Lids, Plates, Trays, Tubs',
# MAGIC     0.11,
# MAGIC     'ILLUSTRATIVE_LOW',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Provisional cap/lid mapping.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA2027-HIGH-PP-P41P',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_P41P',
# MAGIC     'PP (#5)',
# MAGIC     'Other Rigid Containers, Cups, Lids, Plates, Trays, Tubs',
# MAGIC     0.24,
# MAGIC     'ILLUSTRATIVE_HIGH',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Provisional cap/lid mapping.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA2027-LOW-CORR-PF9N',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_PF9N',
# MAGIC     'Cardboard',
# MAGIC     'Cardboard w/o plastic component',
# MAGIC     0.02,
# MAGIC     'ILLUSTRATIVE_LOW',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Provisional secondary corrugated case classification.',
# MAGIC     current_timestamp()
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'CA2027-HIGH-CORR-PF9N',
# MAGIC     'California',
# MAGIC     'SB 54',
# MAGIC     2027,
# MAGIC     '25_PF9N',
# MAGIC     'Cardboard',
# MAGIC     'Cardboard w/o plastic component',
# MAGIC     0.05,
# MAGIC     'ILLUSTRATIVE_HIGH',
# MAGIC     'CAA California Illustrative Fees - Revised May 2026',
# MAGIC     NULL,
# MAGIC     DATE '2026-05-28',
# MAGIC     'CAA_ILLUSTRATIVE',
# MAGIC     'Provisional secondary corrugated case classification.',
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_illustrative_epr_cost AS
# MAGIC
# MAGIC WITH basis AS (
# MAGIC     SELECT *
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis
# MAGIC ),
# MAGIC
# MAGIC calc AS (
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
# MAGIC     FROM basis
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     annual_total_pet_bottle_kg,
# MAGIC     annual_pp_cap_kg,
# MAGIC     annual_containerboard_kg,
# MAGIC
# MAGIC     /* LOW */
# MAGIC
# MAGIC     pet_lb * (0.13 + 0.04 + 0.17)
# MAGIC       + annual_units_sold * 0.001
# MAGIC       AS pet_fee_low_usd,
# MAGIC
# MAGIC     pp_lb * (0.11 + 0.04 + 0.17)
# MAGIC       + annual_units_sold * 0.001
# MAGIC       AS pp_cap_fee_low_usd,
# MAGIC
# MAGIC     corrugated_lb * 0.02
# MAGIC       AS corrugated_fee_low_usd,
# MAGIC
# MAGIC     /* HIGH */
# MAGIC
# MAGIC     pet_lb * (0.38 + 0.10 + 0.25)
# MAGIC       + annual_units_sold * 0.0012
# MAGIC       AS pet_fee_high_usd,
# MAGIC
# MAGIC     pp_lb * (0.24 + 0.10 + 0.25)
# MAGIC       + annual_units_sold * 0.0012
# MAGIC       AS pp_cap_fee_high_usd,
# MAGIC
# MAGIC     corrugated_lb * 0.05
# MAGIC       AS corrugated_fee_high_usd
# MAGIC
# MAGIC FROM calc;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_scenario_cost_summary AS
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     pet_fee_low_usd
# MAGIC       + pp_cap_fee_low_usd
# MAGIC       + corrugated_fee_low_usd
# MAGIC       AS total_epr_low_usd,
# MAGIC
# MAGIC     pet_fee_high_usd
# MAGIC       + pp_cap_fee_high_usd
# MAGIC       + corrugated_fee_high_usd
# MAGIC       AS total_epr_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_ca_illustrative_epr_cost;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     total_epr_low_usd,
# MAGIC     total_epr_high_usd
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_cost_summary
# MAGIC ORDER BY scenario_id;