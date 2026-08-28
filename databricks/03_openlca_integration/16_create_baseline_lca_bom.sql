-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.baseline_lca_bom (
    bom_id STRING,

    sku_id STRING,
    manufacturer_sku STRING,
    product_name STRING,

    scenario_id STRING,
    scenario_name STRING,

    component_id STRING,
    packaging_component STRING,
    packaging_level STRING,

    material_type STRING,

    component_mass_g_per_package DOUBLE,
    component_mass_kg_per_package DOUBLE,

    mass_value_origin STRING,
    mass_data_quality STRING,

    lci_dataset_id STRING,
    lci_process_uuid STRING,
    lci_process_name STRING,
    lci_database STRING,

    lci_mapping_status STRING,
    lci_mapping_basis STRING,

    applicability_status STRING,

    reviewer_note STRING,
    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.gold.baseline_lca_bom
VALUES

(
    'BOM-BL-BOTTLE',

    'SKU-KH-20OZ',
    '00013000051200',
    'Heinz Tomato Ketchup 20 oz',

    'S0',
    'Baseline',

    'COMP-BOTTLE',
    'Bottle',
    'Primary',

    'PET',

    30.0,
    0.030,

    'ASSUMPTION_RECONCILED',
    'Medium',

    'DATA-PET-001',
    '2b2f738d-2044-462f-ba56-5112ee683cb6',
    'Polyethylene terephthalate, PET; virgin resin; at plant',
    'USLCI',

    'RESOLVED',
    'Direct material match to PET bottle; current free USLCI process previously validated.',

    'APPROVED_BASELINE',

    'Bottle material is verified PET. Mass remains an assumption, but total packaging mass has been externally reconciled against published gross-minus-net case weight.',

    current_timestamp()
),

(
    'BOM-BL-CAP',

    'SKU-KH-20OZ',
    '00013000051200',
    'Heinz Tomato Ketchup 20 oz',

    'S0',
    'Baseline',

    'COMP-CAP',
    'Cap',
    'Primary',

    'PP',

    4.0,
    0.004,

    'ASSUMPTION',
    'Low',

    NULL,
    NULL,
    NULL,
    'USLCI',

    'UNRESOLVED',
    'PP material supported by packaging evidence, but exact current free USLCI process has not yet been selected.',

    'PROVISIONAL',

    'Do not substitute a guessed polypropylene process UUID. Resolve the exact USLCI process before openLCA calculation.',

    current_timestamp()
),

(
    'BOM-BL-LABEL',

    'SKU-KH-20OZ',
    '00013000051200',
    'Heinz Tomato Ketchup 20 oz',

    'S0',
    'Baseline',

    'COMP-LABEL',
    'Label',
    'Primary',

    NULL,

    1.0,
    0.001,

    'ASSUMPTION',
    'Low',

    NULL,
    NULL,
    NULL,
    NULL,

    'BLOCKED',
    'Label material is currently unknown.',

    'NOT_READY',

    'Do not assign a plastic-film or paper proxy until an explicit modeling assumption is approved.',

    current_timestamp()
),

(
    'BOM-BL-CASE',

    'SKU-KH-20OZ',
    '00013000051200',
    'Heinz Tomato Ketchup 20 oz',

    'S0',
    'Baseline',

    'COMP-CASE',
    'Corrugated case allocation',
    'Secondary',

    'Corrugated board',

    18.0,
    0.018,

    'ASSUMPTION_RECONCILED',
    'Medium-Low',

    NULL,
    NULL,
    NULL,
    'USLCI',

    'UNRESOLVED',
    'Current product specification supports box/carton shipment packaging, but exact free LCI process has not yet been selected.',

    'PROVISIONAL',

    'Resolve the exact corrugated/containerboard process from the current USLCI repository before calculation.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    component_mass_g_per_package,
    lci_process_name,
    lci_mapping_status,
    applicability_status,
    mass_data_quality
FROM kraft_heinz_lca.gold.baseline_lca_bom
ORDER BY component_id;

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    component_mass_kg_per_package,
    lci_mapping_status
FROM kraft_heinz_lca.gold.baseline_lca_bom
WHERE lci_mapping_status <> 'RESOLVED';

-- COMMAND ----------

SELECT
    SUM(component_mass_g_per_package) AS baseline_bom_mass_g
FROM kraft_heinz_lca.gold.baseline_lca_bom
WHERE scenario_id = 'S0';

-- COMMAND ----------

SELECT
    b.baseline_bom_mass_g,
    ROUND(AVG(v.inferred_packaging_g_per_unit), 2)
        AS avg_external_validation_g,

    ROUND(
        b.baseline_bom_mass_g
        - AVG(v.inferred_packaging_g_per_unit),
        2
    ) AS difference_g

FROM (
    SELECT
        SUM(component_mass_g_per_package) AS baseline_bom_mass_g
    FROM kraft_heinz_lca.gold.baseline_lca_bom
    WHERE scenario_id = 'S0'
) b

CROSS JOIN kraft_heinz_lca.silver.packaging_mass_validation v

GROUP BY b.baseline_bom_mass_g;