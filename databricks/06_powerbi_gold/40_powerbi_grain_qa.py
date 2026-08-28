# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     'decision_rank' AS source_table,
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'scenario_master',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'lca_scenario_summary',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_basis',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_cost',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'procurement',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_savings_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC ORDER BY source_table, scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all AS
# MAGIC
# MAGIC /* Existing scenarios, but explicitly exclude S3 */
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     annual_units_sold,
# MAGIC     annual_total_pet_bottle_kg,
# MAGIC     annual_virgin_pet_kg,
# MAGIC     annual_rpet_kg,
# MAGIC     annual_pp_cap_kg,
# MAGIC     annual_containerboard_kg
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis
# MAGIC
# MAGIC WHERE scenario_id <> 'S3'
# MAGIC
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC
# MAGIC /* Canonical S3 definition */
# MAGIC SELECT
# MAGIC     'S3' AS scenario_id,
# MAGIC     '10% Lightweighting + 30% rPET' AS scenario_name,
# MAGIC
# MAGIC     5000000 AS annual_units_sold,
# MAGIC
# MAGIC     135000.0 AS annual_total_pet_bottle_kg,
# MAGIC     94500.0  AS annual_virgin_pet_kg,
# MAGIC     40500.0  AS annual_rpet_kg,
# MAGIC
# MAGIC     20000.0  AS annual_pp_cap_kg,
# MAGIC     90000.0  AS annual_containerboard_kg;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC GROUP BY scenario_id
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     'decision_rank' AS source_table,
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'scenario_master',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'lca_scenario_summary',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_basis',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_cost',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'procurement',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_savings_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC ORDER BY source_table, scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT scenario_id) AS distinct_scenarios
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     'decision_rank' AS source_table,
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'scenario_master',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'lca_scenario_summary',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_basis',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_cost',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'procurement',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_savings_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC ORDER BY source_table, scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC (
# MAGIC     scenario_result_id,
# MAGIC     model_id,
# MAGIC     sku_id,
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     functional_unit,
# MAGIC     modeled_packaging_mass_kg,
# MAGIC     impact_method,
# MAGIC     impact_category,
# MAGIC     impact_unit,
# MAGIC     impact_result,
# MAGIC     baseline_impact_result,
# MAGIC     avoided_impact_per_unit,
# MAGIC     reduction_pct,
# MAGIC     result_source,
# MAGIC     result_status,
# MAGIC     data_classification,
# MAGIC     limitation_note,
# MAGIC     calculated_at
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     'LCA-S0-GWP-001',
# MAGIC     'OLCA-KH-S0-001',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S0',
# MAGIC     'Baseline',
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC     0.052,
# MAGIC     'TRACI 2.2',
# MAGIC     'Global warming',
# MAGIC     'kg CO2 eq',
# MAGIC     0.10532,
# MAGIC     0.10532,
# MAGIC     0.0,
# MAGIC     0.0,
# MAGIC     'openLCA 2.6.1',
# MAGIC     'VERIFIED_MODEL_RESULT',
# MAGIC     'BASELINE_MODEL',
# MAGIC     'Screening cradle-to-gate packaging-material model. Label excluded. Bottle forming, cap molding, corrugating/converting, filling, distribution, use, and end-of-life excluded.',
# MAGIC     current_timestamp()
# MAGIC
# MAGIC WHERE NOT EXISTS (
# MAGIC     SELECT 1
# MAGIC     FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC     WHERE scenario_id = 'S0'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC GROUP BY scenario_id
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT scenario_id) AS distinct_scenarios
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE TABLE kraft_heinz_lca.gold.packaging_decision_powerbi
# MAGIC USING DELTA
# MAGIC AS
# MAGIC
# MAGIC SELECT
# MAGIC     r.scenario_id,
# MAGIC     r.scenario_name,
# MAGIC
# MAGIC     /* =========================
# MAGIC        LCA / CLIMATE
# MAGIC        ========================= */
# MAGIC     r.gwp_reduction_pct,
# MAGIC     r.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     l.modeled_packaging_mass_kg,
# MAGIC     l.impact_result
# MAGIC         AS gwp_kg_co2e_per_package,
# MAGIC
# MAGIC     l.avoided_impact_per_unit
# MAGIC         AS avoided_gwp_kg_co2e_per_package,
# MAGIC
# MAGIC     l.impact_method,
# MAGIC     l.functional_unit,
# MAGIC     l.result_source,
# MAGIC
# MAGIC     l.result_status
# MAGIC         AS lca_result_status,
# MAGIC
# MAGIC     l.data_classification
# MAGIC         AS lca_data_classification,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        MATERIAL / CIRCULARITY
# MAGIC        ========================= */
# MAGIC     r.annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     s.annual_plastic_source_reduction_kg,
# MAGIC
# MAGIC     r.annual_rpet_requirement_kg,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        MARKET / PACKAGING BASIS
# MAGIC        ========================= */
# MAGIC     m.annual_units_sold,
# MAGIC
# MAGIC     m.annual_total_pet_bottle_kg,
# MAGIC     m.annual_virgin_pet_kg,
# MAGIC     m.annual_rpet_kg,
# MAGIC
# MAGIC     m.annual_pp_cap_kg,
# MAGIC     m.annual_containerboard_kg,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        CALIFORNIA SB 54 EPR
# MAGIC        ========================= */
# MAGIC     e.total_epr_low_usd,
# MAGIC     e.total_epr_high_usd,
# MAGIC
# MAGIC     e.annual_epr_savings_low_usd,
# MAGIC     e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        PROCUREMENT
# MAGIC        ========================= */
# MAGIC     p.material_savings_low_usd,
# MAGIC     p.material_savings_high_usd,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        OPERATING / FP&A
# MAGIC        ========================= */
# MAGIC     r.annual_operating_value_min_usd,
# MAGIC     r.annual_operating_value_max_usd,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        DECISION RANKING
# MAGIC        ========================= */
# MAGIC     r.carbon_rank,
# MAGIC     r.virgin_plastic_rank,
# MAGIC     r.conservative_financial_rank,
# MAGIC
# MAGIC     r.operating_case_status,
# MAGIC     r.decision_category,
# MAGIC
# MAGIC
# MAGIC     /* =========================
# MAGIC        MODEL / GOVERNANCE FLAGS
# MAGIC        ========================= */
# MAGIC     CASE
# MAGIC         WHEN r.scenario_id = 'S0'
# MAGIC             THEN 'BASELINE'
# MAGIC         ELSE 'SCENARIO'
# MAGIC     END AS scenario_type,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN r.scenario_id IN ('S1','S2','S3')
# MAGIC             THEN 'SYNTHETIC_SCENARIO_ASSUMPTION'
# MAGIC         ELSE 'BASELINE_MODEL'
# MAGIC     END AS scenario_data_classification,
# MAGIC
# MAGIC     'California'
# MAGIC         AS jurisdiction,
# MAGIC
# MAGIC     2027
# MAGIC         AS epr_fee_year,
# MAGIC
# MAGIC     'CAA California Illustrative Fees - Revised May 2026'
# MAGIC         AS epr_fee_source,
# MAGIC
# MAGIC     'ILLUSTRATIVE_NOT_FINAL'
# MAGIC         AS epr_fee_status,
# MAGIC
# MAGIC     current_timestamp()
# MAGIC         AS gold_generated_at
# MAGIC
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank r
# MAGIC
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_packaging_scenario_master s
# MAGIC
# MAGIC     ON r.scenario_id = s.scenario_id
# MAGIC
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.lca_scenario_summary l
# MAGIC
# MAGIC     ON r.scenario_id = l.scenario_id
# MAGIC
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all m
# MAGIC
# MAGIC     ON r.scenario_id = m.scenario_id
# MAGIC
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_cost_summary_all e
# MAGIC
# MAGIC     ON r.scenario_id = e.scenario_id
# MAGIC
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_pet_procurement_savings_all p
# MAGIC
# MAGIC     ON r.scenario_id = p.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS rows_per_scenario
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi
# MAGIC GROUP BY scenario_id
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     'decision_rank' AS source_table,
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS row_count
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'scenario_master',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'lca_scenario_summary',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_basis',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'epr_cost',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'procurement',
# MAGIC     scenario_id,
# MAGIC     COUNT(*)
# MAGIC FROM kraft_heinz_lca.gold.v_pet_procurement_savings_all
# MAGIC GROUP BY scenario_id
# MAGIC
# MAGIC ORDER BY source_table, scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_result_id,
# MAGIC     model_id,
# MAGIC     impact_result,
# MAGIC     calculated_at
# MAGIC FROM kraft_heinz_lca.gold.lca_scenario_summary
# MAGIC ORDER BY scenario_id, calculated_at;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC WITH grain_check AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         'decision_rank' AS source_table,
# MAGIC         scenario_id,
# MAGIC         COUNT(*) AS row_count
# MAGIC     FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC     GROUP BY scenario_id
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         'scenario_master',
# MAGIC         scenario_id,
# MAGIC         COUNT(*)
# MAGIC     FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC     GROUP BY scenario_id
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         'epr_basis',
# MAGIC         scenario_id,
# MAGIC         COUNT(*)
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC     GROUP BY scenario_id
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         'epr_cost',
# MAGIC         scenario_id,
# MAGIC         COUNT(*)
# MAGIC     FROM kraft_heinz_lca.gold.v_ca_epr_cost_summary_all
# MAGIC     GROUP BY scenario_id
# MAGIC
# MAGIC     UNION ALL
# MAGIC
# MAGIC     SELECT
# MAGIC         'procurement',
# MAGIC         scenario_id,
# MAGIC         COUNT(*)
# MAGIC     FROM kraft_heinz_lca.gold.v_pet_procurement_savings_all
# MAGIC     GROUP BY scenario_id
# MAGIC )
# MAGIC
# MAGIC SELECT *
# MAGIC FROM grain_check
# MAGIC WHERE row_count <> 1
# MAGIC ORDER BY source_table, scenario_id;