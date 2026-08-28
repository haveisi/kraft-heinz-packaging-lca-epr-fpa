# Databricks notebook source
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
# MAGIC     /* LCA */
# MAGIC     r.gwp_reduction_pct,
# MAGIC     r.annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     /* MATERIAL / CIRCULARITY */
# MAGIC     r.annual_virgin_pet_displacement_kg,
# MAGIC     s.annual_plastic_source_reduction_kg,
# MAGIC     r.annual_rpet_requirement_kg,
# MAGIC
# MAGIC     /* FINANCIAL RANGE */
# MAGIC     r.annual_operating_value_min_usd,
# MAGIC     r.annual_operating_value_max_usd,
# MAGIC
# MAGIC     /* RANKING */
# MAGIC     r.carbon_rank,
# MAGIC     r.virgin_plastic_rank,
# MAGIC     r.conservative_financial_rank,
# MAGIC     r.operating_case_status,
# MAGIC     r.decision_category,
# MAGIC
# MAGIC     /* LCA RESULT DETAIL */
# MAGIC     l.modeled_packaging_mass_kg,
# MAGIC     l.impact_result AS gwp_kg_co2e_per_package,
# MAGIC     l.avoided_impact_per_unit AS avoided_gwp_kg_co2e_per_package,
# MAGIC     l.impact_method,
# MAGIC     l.functional_unit,
# MAGIC     l.result_source,
# MAGIC     l.result_status AS lca_result_status,
# MAGIC     l.data_classification AS lca_data_classification,
# MAGIC
# MAGIC     /* MARKET BASIS */
# MAGIC     m.annual_units_sold,
# MAGIC     m.annual_total_pet_bottle_kg,
# MAGIC     m.annual_virgin_pet_kg,
# MAGIC     m.annual_rpet_kg,
# MAGIC     m.annual_pp_cap_kg,
# MAGIC     m.annual_containerboard_kg,
# MAGIC
# MAGIC     /* EPR */
# MAGIC     e.total_epr_low_usd,
# MAGIC     e.total_epr_high_usd,
# MAGIC     e.annual_epr_savings_low_usd,
# MAGIC     e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC     /* PROCUREMENT */
# MAGIC     p.material_savings_low_usd,
# MAGIC     p.material_savings_high_usd,
# MAGIC
# MAGIC     /* CONTROL FLAGS */
# MAGIC     CASE
# MAGIC         WHEN r.scenario_id = 'S0'
# MAGIC         THEN 'BASELINE'
# MAGIC         ELSE 'SCENARIO'
# MAGIC     END AS scenario_type,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN r.scenario_id IN ('S1','S2','S3')
# MAGIC         THEN 'SYNTHETIC_SCENARIO_ASSUMPTION'
# MAGIC         ELSE 'BASELINE_MODEL'
# MAGIC     END AS scenario_data_classification,
# MAGIC
# MAGIC     'California' AS jurisdiction,
# MAGIC
# MAGIC     2027 AS epr_fee_year,
# MAGIC
# MAGIC     'CAA California Illustrative Fees - Revised May 2026'
# MAGIC         AS epr_fee_source,
# MAGIC
# MAGIC     'ILLUSTRATIVE_NOT_FINAL'
# MAGIC         AS epr_fee_status,
# MAGIC
# MAGIC     current_timestamp() AS gold_generated_at
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank r
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_packaging_scenario_master s
# MAGIC     ON r.scenario_id = s.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.lca_scenario_summary l
# MAGIC     ON r.scenario_id = l.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all m
# MAGIC     ON r.scenario_id = m.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_cost_summary_all e
# MAGIC     ON r.scenario_id = e.scenario_id
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.v_pet_procurement_savings_all p
# MAGIC     ON r.scenario_id = p.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_kg_co2e_per_package,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_rpet_requirement_kg,
# MAGIC     annual_operating_value_min_usd,
# MAGIC     annual_operating_value_max_usd,
# MAGIC     decision_category,
# MAGIC     epr_fee_status,
# MAGIC     scenario_data_classification
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT scenario_id) AS distinct_scenarios
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi;