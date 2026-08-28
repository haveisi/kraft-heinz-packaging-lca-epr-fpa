# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_financial_sensitivity AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_rpet_kg,
# MAGIC
# MAGIC     'A_RPET_LOW_EPR_LOW' AS sensitivity_case,
# MAGIC     material_savings_low_usd AS material_savings_usd,
# MAGIC     annual_epr_savings_low_usd AS epr_savings_usd,
# MAGIC
# MAGIC     material_savings_low_usd
# MAGIC       + annual_epr_savings_low_usd
# MAGIC         AS annual_operating_value_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_integrated_operating_case
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_rpet_kg,
# MAGIC
# MAGIC     'B_RPET_LOW_EPR_HIGH',
# MAGIC     material_savings_low_usd,
# MAGIC     annual_epr_savings_high_usd,
# MAGIC
# MAGIC     material_savings_low_usd
# MAGIC       + annual_epr_savings_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_integrated_operating_case
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_rpet_kg,
# MAGIC
# MAGIC     'C_RPET_HIGH_EPR_LOW',
# MAGIC     material_savings_high_usd,
# MAGIC     annual_epr_savings_low_usd,
# MAGIC
# MAGIC     material_savings_high_usd
# MAGIC       + annual_epr_savings_low_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_integrated_operating_case
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_plastic_source_reduction_kg,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_rpet_kg,
# MAGIC
# MAGIC     'D_RPET_HIGH_EPR_HIGH',
# MAGIC     material_savings_high_usd,
# MAGIC     annual_epr_savings_high_usd,
# MAGIC
# MAGIC     material_savings_high_usd
# MAGIC       + annual_epr_savings_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_integrated_operating_case;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_financial_sensitivity
# MAGIC ORDER BY scenario_id, sensitivity_case;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_decision_summary AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     MAX(scenario_name) AS scenario_name,
# MAGIC
# MAGIC     MAX(gwp_reduction_pct) AS gwp_reduction_pct,
# MAGIC     MAX(annual_avoided_gwp_tco2e) AS annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     MAX(annual_plastic_source_reduction_kg)
# MAGIC         AS annual_plastic_source_reduction_kg,
# MAGIC
# MAGIC     MAX(annual_virgin_pet_displacement_kg)
# MAGIC         AS annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     MAX(annual_rpet_kg)
# MAGIC         AS annual_rpet_requirement_kg,
# MAGIC
# MAGIC     MIN(annual_operating_value_usd)
# MAGIC         AS annual_operating_value_min_usd,
# MAGIC
# MAGIC     MAX(annual_operating_value_usd)
# MAGIC         AS annual_operating_value_max_usd,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN MIN(annual_operating_value_usd) > 0
# MAGIC             THEN 'POSITIVE_ACROSS_TESTED_CASES'
# MAGIC
# MAGIC         WHEN MAX(annual_operating_value_usd) < 0
# MAGIC             THEN 'NEGATIVE_ACROSS_TESTED_CASES'
# MAGIC
# MAGIC         ELSE 'SENSITIVE_TO_ASSUMPTIONS'
# MAGIC     END AS operating_case_status
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_financial_sensitivity
# MAGIC
# MAGIC GROUP BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_summary
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_decision_rank AS
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     RANK() OVER (
# MAGIC         ORDER BY gwp_reduction_pct DESC
# MAGIC     ) AS carbon_rank,
# MAGIC
# MAGIC     RANK() OVER (
# MAGIC         ORDER BY annual_virgin_pet_displacement_kg DESC
# MAGIC     ) AS virgin_plastic_rank,
# MAGIC
# MAGIC     RANK() OVER (
# MAGIC         ORDER BY annual_operating_value_min_usd DESC
# MAGIC     ) AS conservative_financial_rank,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN operating_case_status = 'POSITIVE_ACROSS_TESTED_CASES'
# MAGIC          AND gwp_reduction_pct >= 10
# MAGIC         THEN 'STRONG_INTEGRATED_CASE'
# MAGIC
# MAGIC         WHEN operating_case_status = 'POSITIVE_ACROSS_TESTED_CASES'
# MAGIC         THEN 'VALUE_CREATING_EFFICIENCY_CASE'
# MAGIC
# MAGIC         WHEN operating_case_status = 'NEGATIVE_ACROSS_TESTED_CASES'
# MAGIC          AND gwp_reduction_pct > 0
# MAGIC         THEN 'STRATEGIC_CIRCULARITY_CASE'
# MAGIC
# MAGIC         ELSE 'BASELINE_OR_REVIEW'
# MAGIC     END AS decision_category
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e,
# MAGIC     annual_virgin_pet_displacement_kg,
# MAGIC     annual_operating_value_min_usd,
# MAGIC     annual_operating_value_max_usd,
# MAGIC     carbon_rank,
# MAGIC     conservative_financial_rank,
# MAGIC     operating_case_status,
# MAGIC     decision_category
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_rank
# MAGIC
# MAGIC ORDER BY scenario_id;