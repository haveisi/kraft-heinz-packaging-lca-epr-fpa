-- Databricks notebook source
CREATE SCHEMA IF NOT EXISTS kraft_heinz_lca.gold;

-- COMMAND ----------

SHOW SCHEMAS IN kraft_heinz_lca;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.packaging_master (
    sku_id STRING,
    product_name STRING,
    brand STRING,

    component_id STRING,
    packaging_component STRING,
    packaging_level STRING,

    material_family STRING,
    material_type STRING,

    mass_g_per_unit DOUBLE,
    recycled_content_pct DOUBLE,

    recyclability_status STRING,
    epr_material_category STRING,

    supplier_name STRING,
    plant_name STRING,

    market_state STRING,
    annual_units_sold DOUBLE,

    unit_cost_usd DOUBLE,

    evidence_id STRING,
    evidence_status STRING,
    value_origin STRING,

    data_quality_status STRING,
    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

SHOW TABLES IN kraft_heinz_lca.gold;

-- COMMAND ----------

SELECT COUNT(*) AS packaging_master_rows
FROM kraft_heinz_lca.gold.packaging_master;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.gold.packaging_master
VALUES

(
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Heinz',

    'COMP-BOTTLE',
    'Bottle',
    'Primary',

    'Plastic',
    'PET',

    30.0,
    NULL,

    'Recyclable design supported qualitatively',
    'Rigid plastic packaging',

    NULL,
    NULL,

    NULL,
    NULL,

    NULL,

    'KH20-001',
    'Direct evidence for PET material; mass is assumption',
    'MIXED',

    'Needs Improvement',

    'PET material and single-layer structure are directly supported. Bottle mass of 30 g is a training assumption and must remain flagged.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Heinz',

    'COMP-CAP',
    'Cap',
    'Primary',

    'Plastic',
    NULL,

    4.0,
    NULL,

    'Unknown',
    'Rigid plastic packaging',

    NULL,
    NULL,

    NULL,
    NULL,

    NULL,

    NULL,
    'No direct material evidence; mass assumption only',
    'ASSUMPTION',

    'Low',

    'Cap material is not yet supported. Do not assume PP until evidence or approved proxy is established.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Heinz',

    'COMP-LABEL',
    'Label',
    'Primary',

    NULL,
    NULL,

    1.0,
    NULL,

    'Unknown',
    NULL,

    NULL,
    NULL,

    NULL,
    NULL,

    NULL,

    NULL,
    'Mass assumption only',
    'ASSUMPTION',

    'Low',

    'Label material and actual mass are not directly supported.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Heinz',

    'COMP-CASE',
    'Corrugated case allocation',
    'Secondary',

    'Paper',
    'Corrugated board',

    18.0,
    NULL,

    'Typically recyclable; not yet product-specific',
    'Paper and fiber packaging',

    NULL,
    NULL,

    NULL,
    NULL,

    NULL,

    NULL,
    'Training assumption',
    'ASSUMPTION',

    'Low',

    'Secondary packaging material and allocated 18 g per unit are training assumptions pending case configuration evidence.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    mass_g_per_unit,
    value_origin,
    data_quality_status
FROM kraft_heinz_lca.gold.packaging_master
ORDER BY component_id;

-- COMMAND ----------

SELECT
    SUM(mass_g_per_unit) AS total_packaging_mass_g
FROM kraft_heinz_lca.gold.packaging_master;