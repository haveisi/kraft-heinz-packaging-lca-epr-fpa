-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.lca_dataset_registry (
    dataset_id STRING,

    database_name STRING,
    database_release STRING,

    process_name STRING,
    process_uuid STRING,

    reference_flow STRING,
    reference_amount DOUBLE,
    reference_unit STRING,

    geography STRING,
    data_year STRING,

    process_type STRING,

    dataset_owner STRING,
    data_generator STRING,
    source_publication STRING,

    access_status STRING,
    license_status STRING,
    allowed_for_project BOOLEAN,

    intended_use STRING,
    target_lci_field STRING,

    data_quality_note STRING,
    methodological_note STRING,

    source_url STRING,

    review_status STRING,
    reviewer_note STRING,

    retrieval_date DATE
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.lca_dataset_registry
VALUES
(
    'DATA-PET-001',

    'USLCI / Federal LCA Commons',

    'USLCI v1.2026-06.0',

    'Polyethylene terephthalate, PET; virgin resin; at plant',

    '2b2f738d-2044-462f-ba56-5112ee683cb6',

    'Polyethylene terephthalate, PET; virgin resin; at plant',

    1.0,

    'kg',

    'United States / North American production represented',

    '2022',

    'Unit process',

    'NAPCOR',

    'ERG',

    'ERG (2026) Cradle-To-Resin Life Cycle Analysis of Virgin, Recycled, and Blend Polyethylene Terephthalate (PET) Resin for NAPCOR',

    'Free public access',

    'USLCI/Federal LCA Commons terms of use',

    TRUE,

    'Baseline virgin PET resin production for Heinz ketchup bottle LCA',

    'primary_container_material',

    'Primary data were collected from four producers operating nine plants in North America: seven U.S. plants, one Canadian plant, and one Mexican plant. Approximately 50 percent of available North American PET resin production capacity was represented.',

    'Dataset represents resin at plant. It does not by itself represent bottle forming, filling, cap, label, transport to Kraft Heinz, or end of life.',

    'https://lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/dataset/PROCESS/2b2f738d-2044-462f-ba56-5112ee683cb6',

    'Approved',

    'Selected as the preferred free process-LCI source for virgin PET because it is current, U.S./North-America relevant, process-based, and explicitly applicable to PET resin production.',

    current_date()
);

-- COMMAND ----------

SELECT
    dataset_id,
    database_name,
    database_release,
    process_name,
    process_uuid,
    reference_amount,
    reference_unit,
    geography,
    data_year,
    access_status,
    allowed_for_project,
    review_status
FROM kraft_heinz_lca.silver.lca_dataset_registry;

-- COMMAND ----------

CREATE VOLUME IF NOT EXISTS kraft_heinz_lca.bronze.lca_reference_data;

-- COMMAND ----------

