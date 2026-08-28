# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW kraft_heinz_lca.gold.v_openlca_baseline_export AS
# MAGIC
# MAGIC SELECT
# MAGIC     bom_id,
# MAGIC
# MAGIC     sku_id,
# MAGIC     manufacturer_sku,
# MAGIC     product_name,
# MAGIC
# MAGIC     scenario_id,
# MAGIC     scenario_name,
# MAGIC
# MAGIC     component_id,
# MAGIC     packaging_component,
# MAGIC     packaging_level,
# MAGIC
# MAGIC     material_type,
# MAGIC
# MAGIC     component_mass_g_per_package,
# MAGIC     component_mass_kg_per_package,
# MAGIC
# MAGIC     lci_dataset_id,
# MAGIC     lci_process_uuid,
# MAGIC     lci_process_name,
# MAGIC     lci_database,
# MAGIC
# MAGIC     lci_mapping_status,
# MAGIC     applicability_status,
# MAGIC
# MAGIC     mass_value_origin,
# MAGIC     mass_data_quality,
# MAGIC
# MAGIC     reviewer_note
# MAGIC
# MAGIC FROM kraft_heinz_lca.gold.baseline_lca_bom
# MAGIC
# MAGIC WHERE scenario_id = 'S0'
# MAGIC
# MAGIC   AND lci_mapping_status IN (
# MAGIC       'RESOLVED',
# MAGIC       'RESOLVED_WITH_PROXY'
# MAGIC   )
# MAGIC
# MAGIC   AND applicability_status IN (
# MAGIC       'APPROVED_BASELINE',
# MAGIC       'APPROVED_SCREENING'
# MAGIC   );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_openlca_baseline_export
# MAGIC ORDER BY component_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM kraft_heinz_lca.gold.v_openlca_baseline_export
# MAGIC WHERE
# MAGIC        lci_process_uuid IS NULL
# MAGIC     OR lci_process_name IS NULL
# MAGIC     OR component_mass_kg_per_package IS NULL
# MAGIC     OR component_mass_kg_per_package <= 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(component_mass_kg_per_package)
# MAGIC         AS modeled_packaging_kg_per_package
# MAGIC FROM kraft_heinz_lca.gold.v_openlca_baseline_export;

# COMMAND ----------

export_df = spark.sql("""
SELECT *
FROM kraft_heinz_lca.gold.v_openlca_baseline_export
ORDER BY component_id
""")

display(export_df)

# COMMAND ----------

export_path = (
    "/Volumes/kraft_heinz_lca/"
    "bronze/lca_reference_data/"
    "openlca_baseline_export"
)

(
    export_df
    .coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(export_path)
)

print(export_path)

# COMMAND ----------

files = dbutils.fs.ls(export_path)

for f in files:
    print(f.name, f.path)

# COMMAND ----------

part_file = [
    f.path
    for f in dbutils.fs.ls(export_path)
    if f.name.startswith("part-")
][0]

final_csv = (
    "/Volumes/kraft_heinz_lca/"
    "bronze/lca_reference_data/"
    "kraft_heinz_openlca_baseline.csv"
)

dbutils.fs.cp(
    part_file,
    final_csv
)

print(final_csv)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.openlca_model_control (
# MAGIC     model_id STRING,
# MAGIC
# MAGIC     sku_id STRING,
# MAGIC     scenario_id STRING,
# MAGIC
# MAGIC     model_scope STRING,
# MAGIC     reference_unit STRING,
# MAGIC
# MAGIC     modeled_packaging_mass_kg DOUBLE,
# MAGIC     excluded_packaging_mass_kg DOUBLE,
# MAGIC
# MAGIC     included_components STRING,
# MAGIC     excluded_components STRING,
# MAGIC
# MAGIC     background_database STRING,
# MAGIC
# MAGIC     model_status STRING,
# MAGIC     limitation_note STRING,
# MAGIC
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO kraft_heinz_lca.gold.openlca_model_control
# MAGIC VALUES (
# MAGIC     'OLCA-KH-S0-001',
# MAGIC
# MAGIC     'SKU-KH-20OZ',
# MAGIC     'S0',
# MAGIC
# MAGIC     'Screening packaging cradle-to-gate material production baseline',
# MAGIC     '1 packaged Heinz Tomato Ketchup 20 oz unit',
# MAGIC
# MAGIC     0.052,
# MAGIC     0.001,
# MAGIC
# MAGIC     'Bottle; Cap; Corrugated case allocation',
# MAGIC
# MAGIC     'Label',
# MAGIC
# MAGIC     'USLCI JSON-LD',
# MAGIC
# MAGIC     'READY_FOR_OPENLCA_BUILD',
# MAGIC
# MAGIC     'Baseline currently includes PET resin production, PP resin production, and containerboard upstream material production. Label is excluded. Bottle forming, cap molding, corrugating/converting, filling, transport, and end-of-life are not yet fully represented.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );