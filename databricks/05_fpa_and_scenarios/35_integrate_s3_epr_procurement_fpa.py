# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC     annual_units_sold,
# MAGIC     annual_total_pet_bottle_kg,
# MAGIC     annual_virgin_pet_kg,
# MAGIC     annual_rpet_kg,
# MAGIC     annual_pp_cap_kg,
# MAGIC     annual_containerboard_kg
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC     'S3' AS scenario_id,
# MAGIC     '10% Lightweighting + 30% rPET' AS scenario_name,
# MAGIC     5000000 AS annual_units_sold,
# MAGIC     135000.0 AS annual_total_pet_bottle_kg,
# MAGIC     94500.0 AS annual_virgin_pet_kg,
# MAGIC     40500.0 AS annual_rpet_kg,
# MAGIC     20000.0 AS annual_pp_cap_kg,
# MAGIC     90000.0 AS annual_containerboard_kg;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all
# MAGIC ORDER BY scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_packaging_scenario_master AS
# MAGIC
# MAGIC SELECT
# MAGIC     m.scenario_id,
# MAGIC     m.scenario_name,
# MAGIC
# MAGIC     m.annual_units_sold,
# MAGIC
# MAGIC     m.annual_total_pet_bottle_kg,
# MAGIC     m.annual_virgin_pet_kg,
# MAGIC     m.annual_rpet_kg,
# MAGIC
# MAGIC     150000 - m.annual_total_pet_bottle_kg
# MAGIC         AS annual_plastic_source_reduction_kg,
# MAGIC
# MAGIC     150000 - m.annual_virgin_pet_kg
# MAGIC         AS annual_virgin_pet_displacement_kg,
# MAGIC
# MAGIC     l.impact_result AS gwp_kg_co2e_per_package,
# MAGIC     l.avoided_impact_per_unit AS avoided_gwp_kg_per_package,
# MAGIC     l.reduction_pct AS gwp_reduction_pct,
# MAGIC
# MAGIC     l.avoided_impact_per_unit
# MAGIC         * m.annual_units_sold / 1000
# MAGIC         AS annual_avoided_gwp_tco2e
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_ca_epr_scenario_basis_all m
# MAGIC
# MAGIC LEFT JOIN kraft_heinz_lca.gold.lca_scenario_summary l
# MAGIC     ON m.scenario_id = l.scenario_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_packaging_scenario_master
# MAGIC ORDER BY scenario_id;
# MAGIC

# COMMAND ----------

