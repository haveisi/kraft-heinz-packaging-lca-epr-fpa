# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_s3_material_basis AS
# MAGIC
# MAGIC SELECT
# MAGIC     'S3' AS scenario_id,
# MAGIC     '10% lightweighting + 30% rPET' AS scenario_name,
# MAGIC
# MAGIC     0.0189 AS virgin_pet_kg_per_package,
# MAGIC     0.0081 AS rpet_kg_per_package,
# MAGIC
# MAGIC     0.0270 AS total_pet_bottle_kg_per_package,
# MAGIC
# MAGIC     0.0040 AS pp_cap_kg_per_package,
# MAGIC     0.0180 AS containerboard_kg_per_package,
# MAGIC
# MAGIC     0.0490 AS modeled_packaging_mass_kg,
# MAGIC
# MAGIC     'SYNTHETIC_SCENARIO_ASSUMPTION' AS scenario_status;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_s3_material_basis;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_s3_california_material AS
# MAGIC
# MAGIC SELECT
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     5000000 AS annual_units_sold,
# MAGIC
# MAGIC     virgin_pet_kg_per_package * 5000000
# MAGIC         AS annual_virgin_pet_kg,
# MAGIC
# MAGIC     rpet_kg_per_package * 5000000
# MAGIC         AS annual_rpet_kg,
# MAGIC
# MAGIC     total_pet_bottle_kg_per_package * 5000000
# MAGIC         AS annual_total_pet_bottle_kg,
# MAGIC
# MAGIC     pp_cap_kg_per_package * 5000000
# MAGIC         AS annual_pp_cap_kg,
# MAGIC
# MAGIC     containerboard_kg_per_package * 5000000
# MAGIC         AS annual_containerboard_kg
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.v_s3_material_basis;