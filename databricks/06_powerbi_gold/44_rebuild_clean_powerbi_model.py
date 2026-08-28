# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE TABLE kraft_heinz_lca.gold.packaging_scenario_basis_clean
# MAGIC USING DELTA
# MAGIC AS
# MAGIC
# MAGIC SELECT * FROM VALUES
# MAGIC
# MAGIC (
# MAGIC     'S0',
# MAGIC     'Baseline',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'California',
# MAGIC     2026,
# MAGIC     5000000,
# MAGIC     150000.0,
# MAGIC     150000.0,
# MAGIC     0.0,
# MAGIC     20000.0,
# MAGIC     90000.0
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'S1',
# MAGIC     'PET Bottle Lightweighting 10%',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'California',
# MAGIC     2026,
# MAGIC     5000000,
# MAGIC     135000.0,
# MAGIC     135000.0,
# MAGIC     0.0,
# MAGIC     20000.0,
# MAGIC     90000.0
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'S2',
# MAGIC     'PET Bottle 30% rPET',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'California',
# MAGIC     2026,
# MAGIC     5000000,
# MAGIC     150000.0,
# MAGIC     105000.0,
# MAGIC     45000.0,
# MAGIC     20000.0,
# MAGIC     90000.0
# MAGIC ),
# MAGIC
# MAGIC (
# MAGIC     'S3',
# MAGIC     '10% Lightweighting + 30% rPET',
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'California',
# MAGIC     2026,
# MAGIC     5000000,
# MAGIC     135000.0,
# MAGIC     94500.0,
# MAGIC     40500.0,
# MAGIC     20000.0,
# MAGIC     90000.0
# MAGIC )
# MAGIC
# MAGIC AS t(
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     sku_id,
# MAGIC     jurisdiction,
# MAGIC     reporting_year,
# MAGIC     annual_units_sold,
# MAGIC     annual_total_pet_bottle_kg,
# MAGIC     annual_virgin_pet_kg,
# MAGIC     annual_rpet_kg,
# MAGIC     annual_pp_cap_kg,
# MAGIC     annual_containerboard_kg
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     COUNT(*) AS rows_per_scenario
# MAGIC FROM kraft_heinz_lca.gold.packaging_scenario_basis_clean
# MAGIC GROUP BY scenario_id
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_lca_clean AS
# MAGIC
# MAGIC SELECT
# MAGIC     b.scenario_id,
# MAGIC     b.scenario_name,
# MAGIC     b.sku_id,
# MAGIC     b.jurisdiction,
# MAGIC     b.reporting_year,
# MAGIC     b.annual_units_sold,
# MAGIC
# MAGIC     b.annual_total_pet_bottle_kg,
# MAGIC     b.annual_virgin_pet_kg,
# MAGIC     b.annual_rpet_kg,
# MAGIC     b.annual_pp_cap_kg,
# MAGIC     b.annual_containerboard_kg,
# MAGIC
# MAGIC     150000.0 - b.annual_total_pet_bottle_kg
# MAGIC         AS annual_plastic_source_reduction_kg,
# MAGIC
# MAGIC     150000.0 - b.annual_virgin_pet_kg
# MAGIC         AS annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     l.modeled_packaging_mass_kg,
# MAGIC
# MAGIC     l.impact_result
# MAGIC         AS gwp_kg_co2e_per_package,
# MAGIC
# MAGIC     l.baseline_impact_result
# MAGIC         AS baseline_gwp_kg_co2e_per_package,
# MAGIC
# MAGIC     l.avoided_impact_per_unit
# MAGIC         AS avoided_gwp_kg_co2e_per_package,
# MAGIC
# MAGIC     l.reduction_pct
# MAGIC         AS gwp_reduction_pct,
# MAGIC
# MAGIC     l.avoided_impact_per_unit
# MAGIC         * b.annual_units_sold / 1000.0
# MAGIC         AS annual_avoided_gwp_tco2e,
# MAGIC
# MAGIC     l.impact_method,
# MAGIC     l.functional_unit,
# MAGIC     l.result_source,
# MAGIC     l.result_status AS lca_result_status,
# MAGIC     l.data_classification AS lca_data_classification
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.packaging_scenario_basis_clean b
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.lca_scenario_summary l
# MAGIC     ON b.scenario_id = l.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     gwp_kg_co2e_per_package,
# MAGIC     gwp_reduction_pct,
# MAGIC     annual_avoided_gwp_tco2e
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_lca_clean
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_clean AS
# MAGIC
# MAGIC WITH calculated AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         b.*,
# MAGIC
# MAGIC         annual_total_pet_bottle_kg * 2.2046226218
# MAGIC             AS pet_lb,
# MAGIC
# MAGIC         annual_pp_cap_kg * 2.2046226218
# MAGIC             AS pp_lb,
# MAGIC
# MAGIC         annual_containerboard_kg * 2.2046226218
# MAGIC             AS corrugated_lb,
# MAGIC
# MAGIC         /* LOW CAA illustrative case */
# MAGIC
# MAGIC         annual_total_pet_bottle_kg * 2.2046226218
# MAGIC             * (0.13 + 0.04 + 0.17)
# MAGIC         + annual_units_sold * 0.001
# MAGIC             AS pet_fee_low_usd,
# MAGIC
# MAGIC         annual_pp_cap_kg * 2.2046226218
# MAGIC             * (0.11 + 0.04 + 0.17)
# MAGIC         + annual_units_sold * 0.001
# MAGIC             AS pp_fee_low_usd,
# MAGIC
# MAGIC         annual_containerboard_kg * 2.2046226218
# MAGIC             * 0.02
# MAGIC             AS corrugated_fee_low_usd,
# MAGIC
# MAGIC         /* HIGH CAA illustrative case */
# MAGIC
# MAGIC         annual_total_pet_bottle_kg * 2.2046226218
# MAGIC             * (0.38 + 0.10 + 0.25)
# MAGIC         + annual_units_sold * 0.0012
# MAGIC             AS pet_fee_high_usd,
# MAGIC
# MAGIC         annual_pp_cap_kg * 2.2046226218
# MAGIC             * (0.24 + 0.10 + 0.25)
# MAGIC         + annual_units_sold * 0.0012
# MAGIC             AS pp_fee_high_usd,
# MAGIC
# MAGIC         annual_containerboard_kg * 2.2046226218
# MAGIC             * 0.05
# MAGIC             AS corrugated_fee_high_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.packaging_scenario_basis_clean b
# MAGIC ),
# MAGIC
# MAGIC totals AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         *,
# MAGIC
# MAGIC         pet_fee_low_usd
# MAGIC             + pp_fee_low_usd
# MAGIC             + corrugated_fee_low_usd
# MAGIC             AS total_epr_low_usd,
# MAGIC
# MAGIC         pet_fee_high_usd
# MAGIC             + pp_fee_high_usd
# MAGIC             + corrugated_fee_high_usd
# MAGIC             AS total_epr_high_usd
# MAGIC
# MAGIC     FROM calculated
# MAGIC ),
# MAGIC
# MAGIC baseline AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         *,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN scenario_id = 'S0'
# MAGIC                 THEN total_epr_low_usd
# MAGIC             END
# MAGIC         ) OVER () AS baseline_epr_low_usd,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN scenario_id = 'S0'
# MAGIC                 THEN total_epr_high_usd
# MAGIC             END
# MAGIC         ) OVER () AS baseline_epr_high_usd
# MAGIC
# MAGIC     FROM totals
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     baseline_epr_low_usd - total_epr_low_usd
# MAGIC         AS annual_epr_savings_low_usd,
# MAGIC
# MAGIC     baseline_epr_high_usd - total_epr_high_usd
# MAGIC         AS annual_epr_savings_high_usd
# MAGIC
# MAGIC FROM baseline;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_pet_procurement_clean AS
# MAGIC
# MAGIC WITH price AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-VPET-2026-MID'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS vpet_usd_per_kg,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-RPET-2026-LOW'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS rpet_low_usd_per_kg,
# MAGIC
# MAGIC         MAX(
# MAGIC             CASE
# MAGIC                 WHEN assumption_id = 'FIN-RPET-2026-HIGH'
# MAGIC                 THEN value
# MAGIC             END
# MAGIC         ) AS rpet_high_usd_per_kg
# MAGIC
# MAGIC     FROM kraft_heinz_lca.silver.financial_assumption_registry
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     b.scenario_id,
# MAGIC     b.scenario_name,
# MAGIC
# MAGIC     b.annual_virgin_pet_kg,
# MAGIC     b.annual_rpet_kg,
# MAGIC
# MAGIC     p.vpet_usd_per_kg,
# MAGIC     p.rpet_low_usd_per_kg,
# MAGIC     p.rpet_high_usd_per_kg,
# MAGIC
# MAGIC     150000.0 * p.vpet_usd_per_kg
# MAGIC         AS baseline_pet_cost_usd,
# MAGIC
# MAGIC     b.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + b.annual_rpet_kg * p.rpet_low_usd_per_kg
# MAGIC         AS scenario_pet_cost_low_usd,
# MAGIC
# MAGIC     b.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC       + b.annual_rpet_kg * p.rpet_high_usd_per_kg
# MAGIC         AS scenario_pet_cost_high_usd,
# MAGIC
# MAGIC     150000.0 * p.vpet_usd_per_kg
# MAGIC       -
# MAGIC     (
# MAGIC         b.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC         + b.annual_rpet_kg * p.rpet_low_usd_per_kg
# MAGIC     )
# MAGIC         AS material_savings_low_usd,
# MAGIC
# MAGIC     150000.0 * p.vpet_usd_per_kg
# MAGIC       -
# MAGIC     (
# MAGIC         b.annual_virgin_pet_kg * p.vpet_usd_per_kg
# MAGIC         + b.annual_rpet_kg * p.rpet_high_usd_per_kg
# MAGIC     )
# MAGIC         AS material_savings_high_usd
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.packaging_scenario_basis_clean b
# MAGIC
# MAGIC CROSS JOIN price p;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_decision_clean AS
# MAGIC
# MAGIC WITH integrated AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         l.*,
# MAGIC
# MAGIC         e.total_epr_low_usd,
# MAGIC         e.total_epr_high_usd,
# MAGIC         e.annual_epr_savings_low_usd,
# MAGIC         e.annual_epr_savings_high_usd,
# MAGIC
# MAGIC         p.material_savings_low_usd,
# MAGIC         p.material_savings_high_usd,
# MAGIC
# MAGIC         /* Four independent sensitivity combinations */
# MAGIC
# MAGIC         p.material_savings_low_usd
# MAGIC           + e.annual_epr_savings_low_usd
# MAGIC             AS operating_value_a_usd,
# MAGIC
# MAGIC         p.material_savings_low_usd
# MAGIC           + e.annual_epr_savings_high_usd
# MAGIC             AS operating_value_b_usd,
# MAGIC
# MAGIC         p.material_savings_high_usd
# MAGIC           + e.annual_epr_savings_low_usd
# MAGIC             AS operating_value_c_usd,
# MAGIC
# MAGIC         p.material_savings_high_usd
# MAGIC           + e.annual_epr_savings_high_usd
# MAGIC             AS operating_value_d_usd
# MAGIC
# MAGIC     FROM kraft_heinz_lca.gold.v_packaging_lca_clean l
# MAGIC
# MAGIC     LEFT JOIN kraft_heinz_lca.gold.v_ca_epr_clean e
# MAGIC         ON l.scenario_id = e.scenario_id
# MAGIC
# MAGIC     LEFT JOIN kraft_heinz_lca.gold.v_pet_procurement_clean p
# MAGIC         ON l.scenario_id = p.scenario_id
# MAGIC ),
# MAGIC
# MAGIC ranges AS (
# MAGIC
# MAGIC     SELECT
# MAGIC         *,
# MAGIC
# MAGIC         LEAST(
# MAGIC             operating_value_a_usd,
# MAGIC             operating_value_b_usd,
# MAGIC             operating_value_c_usd,
# MAGIC             operating_value_d_usd
# MAGIC         ) AS annual_operating_value_min_usd,
# MAGIC
# MAGIC         GREATEST(
# MAGIC             operating_value_a_usd,
# MAGIC             operating_value_b_usd,
# MAGIC             operating_value_c_usd,
# MAGIC             operating_value_d_usd
# MAGIC         ) AS annual_operating_value_max_usd
# MAGIC
# MAGIC     FROM integrated
# MAGIC )
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
# MAGIC         WHEN annual_operating_value_min_usd > 0
# MAGIC         THEN 'POSITIVE_ACROSS_TESTED_CASES'
# MAGIC
# MAGIC         WHEN annual_operating_value_max_usd < 0
# MAGIC         THEN 'NEGATIVE_ACROSS_TESTED_CASES'
# MAGIC
# MAGIC         ELSE 'SENSITIVE_TO_ASSUMPTIONS'
# MAGIC     END AS operating_case_status
# MAGIC
# MAGIC FROM ranges;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE TABLE kraft_heinz_lca.gold.packaging_decision_powerbi
# MAGIC USING DELTA
# MAGIC AS
# MAGIC
# MAGIC SELECT
# MAGIC     *,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN scenario_id = 'S0'
# MAGIC         THEN 'BASELINE'
# MAGIC
# MAGIC         ELSE 'SCENARIO'
# MAGIC     END AS scenario_type,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN scenario_id = 'S0'
# MAGIC         THEN 'BASELINE_MODEL'
# MAGIC
# MAGIC         ELSE 'SYNTHETIC_SCENARIO_ASSUMPTION'
# MAGIC     END AS scenario_data_classification,
# MAGIC
# MAGIC     CASE
# MAGIC         WHEN scenario_id = 'S3'
# MAGIC          AND annual_operating_value_min_usd > 0
# MAGIC         THEN 'STRONG_INTEGRATED_CASE'
# MAGIC
# MAGIC         WHEN scenario_id = 'S1'
# MAGIC          AND annual_operating_value_min_usd > 0
# MAGIC         THEN 'VALUE_CREATING_EFFICIENCY_CASE'
# MAGIC
# MAGIC         WHEN annual_operating_value_max_usd < 0
# MAGIC          AND gwp_reduction_pct > 0
# MAGIC         THEN 'STRATEGIC_CIRCULARITY_CASE'
# MAGIC
# MAGIC         WHEN scenario_id = 'S0'
# MAGIC         THEN 'BASELINE'
# MAGIC
# MAGIC         ELSE 'REVIEW'
# MAGIC     END AS decision_category,
# MAGIC
# MAGIC     2027 AS epr_fee_year,
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
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_decision_clean;

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
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT scenario_id) AS distinct_scenarios
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN COUNT(*) = 4
# MAGIC          AND COUNT(DISTINCT scenario_id) = 4
# MAGIC         THEN 'PASS'
# MAGIC         ELSE 'FAIL'
# MAGIC     END AS grain_qa_status,
# MAGIC
# MAGIC     COUNT(*) AS row_count,
# MAGIC     COUNT(DISTINCT scenario_id) AS distinct_scenarios
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.packaging_decision_powerbi;