-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.gold.market_volume (
    market_volume_id STRING,

    sku_id STRING,
    product_name STRING,

    jurisdiction STRING,
    reporting_year INT,

    annual_units_sold DOUBLE,

    data_classification STRING,
    source_description STRING,

    review_status STRING,
    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.gold.market_volume
VALUES

(
    'MV-KH20-OR-2026',
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Oregon',
    2026,

    1200000,

    'SYNTHETIC',
    'Synthetic state-level sales volume created solely for EPR modeling practice.',

    'Approved for Learning',

    'Not Kraft Heinz reported sales. Must never be presented as actual company market volume.',

    current_timestamp()
),

(
    'MV-KH20-CA-2026',
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'California',
    2026,

    5000000,

    'SYNTHETIC',
    'Synthetic state-level sales volume created solely for EPR modeling practice.',

    'Approved for Learning',

    'Not Kraft Heinz reported sales. Larger synthetic volume used to create a meaningful California scenario.',

    current_timestamp()
),

(
    'MV-KH20-WA-2026',
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'Washington',
    2026,

    1500000,

    'SYNTHETIC',
    'Synthetic state-level sales volume created solely for EPR modeling practice.',

    'Approved for Learning',

    'Not Kraft Heinz reported sales. Used only for modeling program exposure.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    jurisdiction,
    reporting_year,
    annual_units_sold,
    data_classification,
    review_status
FROM kraft_heinz_lca.gold.market_volume
ORDER BY jurisdiction;

-- COMMAND ----------

SELECT *
FROM kraft_heinz_lca.gold.market_volume
WHERE data_classification <> 'SYNTHETIC';

-- COMMAND ----------

CREATE OR REPLACE TABLE kraft_heinz_lca.gold.packaging_placed_on_market AS

SELECT
    mv.market_volume_id,

    mv.sku_id,
    mv.product_name,

    mv.jurisdiction,
    mv.reporting_year,

    pm.component_id,
    pm.packaging_component,
    pm.packaging_level,

    pm.material_family,
    pm.material_type,

    pm.mass_g_per_unit,

    mv.annual_units_sold,

    (
        pm.mass_g_per_unit
        * mv.annual_units_sold
        / 1000.0
    ) AS placed_on_market_kg,

    mv.data_classification AS sales_data_classification,

    pm.value_origin AS packaging_value_origin,
    pm.data_quality_status AS packaging_data_quality,

    pm.epr_material_category,

    current_timestamp() AS calculation_timestamp

FROM kraft_heinz_lca.gold.market_volume mv

JOIN kraft_heinz_lca.gold.packaging_master pm
    ON mv.sku_id = pm.sku_id;

-- COMMAND ----------

SELECT
    jurisdiction,
    packaging_component,
    material_type,
    mass_g_per_unit,
    annual_units_sold,
    placed_on_market_kg
FROM kraft_heinz_lca.gold.packaging_placed_on_market
ORDER BY jurisdiction, packaging_component;

-- COMMAND ----------

SELECT
    jurisdiction,
    material_type,
    SUM(placed_on_market_kg) AS total_placed_on_market_kg
FROM kraft_heinz_lca.gold.packaging_placed_on_market
GROUP BY
    jurisdiction,
    material_type
ORDER BY
    jurisdiction,
    total_placed_on_market_kg DESC;

-- COMMAND ----------

SELECT
    jurisdiction,
    packaging_component,
    mass_g_per_unit,
    placed_on_market_kg,
    material_type,
    epr_material_category,

    CASE
        WHEN material_type IS NULL
            THEN 'BLOCKED - MATERIAL UNKNOWN'

        WHEN epr_material_category IS NULL
            THEN 'BLOCKED - EPR CATEGORY UNKNOWN'

        ELSE 'READY FOR CLASSIFICATION'
    END AS epr_data_status

FROM kraft_heinz_lca.gold.packaging_placed_on_market
ORDER BY jurisdiction, packaging_component;

-- COMMAND ----------

SELECT
    jurisdiction,

    SUM(placed_on_market_kg)
        AS total_packaging_placed_on_market_kg

FROM kraft_heinz_lca.gold.packaging_placed_on_market

GROUP BY jurisdiction
ORDER BY jurisdiction;

-- COMMAND ----------

DELETE FROM kraft_heinz_lca.gold.market_volume;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.gold.market_volume
VALUES
(
    'MV-KH20-CA-2026',
    'SKU-KH-20OZ',
    'Heinz Tomato Ketchup 20 oz',
    'California',
    2026,

    5000000,

    'SYNTHETIC',
    'Synthetic California sales volume created solely for SB 54 EPR modeling practice.',

    'Approved for Learning',

    'Not Kraft Heinz reported sales. Used only to demonstrate California placed-on-market and EPR calculations.',

    current_timestamp()
);

-- COMMAND ----------

CREATE OR REPLACE TABLE kraft_heinz_lca.gold.packaging_placed_on_market AS

SELECT
    mv.market_volume_id,
    mv.sku_id,
    mv.product_name,
    mv.jurisdiction,
    mv.reporting_year,

    pm.component_id,
    pm.packaging_component,
    pm.packaging_level,

    pm.material_family,
    pm.material_type,

    pm.mass_g_per_unit,
    mv.annual_units_sold,

    pm.mass_g_per_unit
        * mv.annual_units_sold
        / 1000.0
        AS placed_on_market_kg,

    mv.data_classification AS sales_data_classification,

    pm.value_origin AS packaging_value_origin,
    pm.data_quality_status AS packaging_data_quality,

    pm.epr_material_category,

    current_timestamp() AS calculation_timestamp

FROM kraft_heinz_lca.gold.market_volume mv
JOIN kraft_heinz_lca.gold.packaging_master pm
    ON mv.sku_id = pm.sku_id;

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    mass_g_per_unit,
    annual_units_sold,
    placed_on_market_kg
FROM kraft_heinz_lca.gold.packaging_placed_on_market
ORDER BY packaging_component;