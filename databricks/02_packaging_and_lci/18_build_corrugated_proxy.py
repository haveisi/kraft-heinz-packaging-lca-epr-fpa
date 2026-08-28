# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.lca_proxy_registry (
# MAGIC     proxy_id STRING,
# MAGIC
# MAGIC     target_component STRING,
# MAGIC     target_material STRING,
# MAGIC
# MAGIC     proxy_process_uuid STRING,
# MAGIC     proxy_process_name STRING,
# MAGIC     proxy_database STRING,
# MAGIC     proxy_geography STRING,
# MAGIC
# MAGIC     proxy_scope STRING,
# MAGIC     missing_process_steps STRING,
# MAGIC
# MAGIC     proxy_quality STRING,
# MAGIC     proxy_status STRING,
# MAGIC
# MAGIC     reviewer_note STRING,
# MAGIC     updated_timestamp TIMESTAMP
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO kraft_heinz_lca.silver.lca_proxy_registry
# MAGIC VALUES (
# MAGIC     'PROXY-CORR-001',
# MAGIC
# MAGIC     'Corrugated case allocation',
# MAGIC     'Corrugated board',
# MAGIC
# MAGIC     'c245a252-0860-41d2-9789-802bab7984ab',
# MAGIC     'Containerboard; at mill',
# MAGIC     'USLCI',
# MAGIC     'United States',
# MAGIC
# MAGIC     'Upstream containerboard material production',
# MAGIC
# MAGIC     'Corrugating, adhesive application, converting, cutting, printing and box forming are not explicitly represented by this proxy.',
# MAGIC
# MAGIC     'MEDIUM',
# MAGIC
# MAGIC     'APPROVED_SCREENING_PROXY',
# MAGIC
# MAGIC     'Use only for screening-level secondary-packaging LCA. Do not describe this process as a finished corrugated box process.',
# MAGIC
# MAGIC     current_timestamp()
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE kraft_heinz_lca.gold.baseline_lca_bom
# MAGIC SET
# MAGIC     lci_dataset_id = 'DATA-CONTBOARD-001',
# MAGIC
# MAGIC     lci_process_uuid =
# MAGIC         'c245a252-0860-41d2-9789-802bab7984ab',
# MAGIC
# MAGIC     lci_process_name =
# MAGIC         'Containerboard; at mill',
# MAGIC
# MAGIC     lci_database = 'USLCI',
# MAGIC
# MAGIC     lci_mapping_status =
# MAGIC         'RESOLVED_WITH_PROXY',
# MAGIC
# MAGIC     lci_mapping_basis =
# MAGIC         'USLCI U.S. containerboard production used as upstream material proxy for corrugated secondary packaging.',
# MAGIC
# MAGIC     applicability_status =
# MAGIC         'APPROVED_SCREENING',
# MAGIC
# MAGIC     reviewer_note =
# MAGIC         'Containerboard process represents upstream board production and includes fiber, recovered OCC, energy and chemical inputs. Corrugating and box-conversion processes remain outside the current screening boundary.',
# MAGIC
# MAGIC     updated_timestamp = current_timestamp()
# MAGIC
# MAGIC WHERE bom_id = 'BOM-BL-CASE';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     packaging_component,
# MAGIC     material_type,
# MAGIC     component_mass_g_per_package,
# MAGIC     lci_process_name,
# MAGIC     lci_mapping_status,
# MAGIC     applicability_status
# MAGIC FROM kraft_heinz_lca.gold.baseline_lca_bom
# MAGIC ORDER BY component_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     ROUND(
# MAGIC         100.0 *
# MAGIC         SUM(
# MAGIC             CASE
# MAGIC                 WHEN lci_mapping_status IN
# MAGIC                     ('RESOLVED', 'RESOLVED_WITH_PROXY')
# MAGIC                 THEN component_mass_g_per_package
# MAGIC                 ELSE 0
# MAGIC             END
# MAGIC         )
# MAGIC         /
# MAGIC         SUM(component_mass_g_per_package),
# MAGIC         1
# MAGIC     ) AS modeled_mass_coverage_pct
# MAGIC FROM kraft_heinz_lca.gold.baseline_lca_bom
# MAGIC WHERE scenario_id = 'S0';