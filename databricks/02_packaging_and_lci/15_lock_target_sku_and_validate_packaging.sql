-- Databricks notebook source
ALTER TABLE kraft_heinz_lca.gold.packaging_master
ADD COLUMNS (
    manufacturer_sku STRING,
    gtin STRING,
    sku_scope_status STRING
);

-- COMMAND ----------

UPDATE kraft_heinz_lca.gold.packaging_master
SET
    manufacturer_sku = '00013000051200',
    gtin = '00013000051200',
    sku_scope_status = 'LOCKED_CURRENT_US_FOODSERVICE_SKU',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ';

-- COMMAND ----------

UPDATE kraft_heinz_lca.silver.packaging_cmc_mapping
SET
    packaging_form = 'Bottles, Jugs, and Jars (Pigmented/Color)',
    candidate_cmc_id = '25_P2P',
    final_cmc_id = '25_P2P',
    classification_status = 'FINAL',
    confidence_status = 'HIGH',
    evidence_status =
        'PET bottle supported by Kraft Heinz evidence; current SKU specification identifies Forever Full solid red bottle.',
    reviewer_note =
        'Corrected from 25_P1P after SKU-level validation. Current selected SKU 00013000051200 is described as a solid red bottle, supporting pigmented/color PET classification.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-BOTTLE';

-- COMMAND ----------

UPDATE kraft_heinz_lca.gold.packaging_master
SET
    evidence_status =
        'PET material supported directly; current selected SKU is specified as Forever Full solid red bottle',
    value_origin = 'VERIFIED-DIRECT',
    data_quality_status = 'High',
    reviewer_note =
        'PET and ketchup bottle structure are supported by Kraft Heinz evidence. SKU-specific current product data identifies the 20 oz Forever Full bottle as solid red. Bottle mass of 30 g remains an assumption.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-BOTTLE';

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.packaging_mass_validation (
    validation_id STRING,
    manufacturer_sku STRING,
    case_pack INT,

    gross_case_weight_lb DOUBLE,
    net_product_weight_lb DOUBLE,

    inferred_total_packaging_g DOUBLE,
    inferred_packaging_g_per_unit DOUBLE,

    evidence_type STRING,
    source_strength STRING,
    source_url STRING,

    modeling_use STRING,
    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.packaging_mass_validation
VALUES (
    'VAL-KH20-30CASE-001',

    '10013000050200',
    30,

    41.25,
    37.50,

    (41.25 - 37.50) * 453.59237,

    ((41.25 - 37.50) * 453.59237) / 30.0,

    'Calculated from published gross-minus-net case weight',
    'VERIFIED-PROXY',

    'Current syndicated Kraft Heinz product specification',

    'BOM reconciliation only',

    'Gross-minus-net difference provides an external check on total packaging allocation but cannot identify individual bottle, cap, label, or corrugated masses.',

    current_timestamp()
);

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.packaging_mass_validation
VALUES (
    'VAL-KH20-12CASE-001',

    '00013000051200',
    12,

    16.58,
    15.01,

    (16.58 - 15.01) * 453.59237,

    ((16.58 - 15.01) * 453.59237) / 12.0,

    'Calculated from published gross-minus-net case weight',
    'VERIFIED-PROXY',

    'Current distributor product specification',

    'BOM reconciliation only',

    'Same selected 20 oz SKU family. Use as external validation rather than direct component mass evidence.',

    current_timestamp()
);

-- COMMAND ----------

WITH current_bom AS (
    SELECT
        SUM(mass_g_per_unit) AS modeled_packaging_g
    FROM kraft_heinz_lca.gold.packaging_master
    WHERE sku_id = 'SKU-KH-20OZ'
)

SELECT
    v.manufacturer_sku,
    v.case_pack,
    ROUND(v.inferred_packaging_g_per_unit, 2)
        AS observed_proxy_packaging_g,

    ROUND(b.modeled_packaging_g, 2)
        AS modeled_packaging_g,

    ROUND(
        b.modeled_packaging_g
        - v.inferred_packaging_g_per_unit,
        2
    ) AS difference_g

FROM kraft_heinz_lca.silver.packaging_mass_validation v
CROSS JOIN current_bom b;