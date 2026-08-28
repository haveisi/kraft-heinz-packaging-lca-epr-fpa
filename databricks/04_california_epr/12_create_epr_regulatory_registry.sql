-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.epr_regulatory_registry (
    jurisdiction STRING,
    program_name STRING,
    regulator STRING,
    pro_name STRING,

    law_or_rule STRING,

    producer_registration_status STRING,
    producer_fee_status STRING,

    program_effective_date DATE,
    producer_fee_start_date DATE,

    packaging_scope STRING,

    source_status STRING,
    source_url STRING,

    data_classification STRING,

    reviewer_note STRING,
    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.epr_regulatory_registry
VALUES

(
    'Oregon',
    'Recycling Modernization Act',
    'Oregon Department of Environmental Quality',
    'Circular Action Alliance',

    'ORS 459A / Recycling Modernization Act',

    'Active',
    'Fees active',

    DATE '2025-07-01',
    DATE '2025-07-01',

    'Packaging, paper and food serviceware covered under Oregon RMA rules',

    'Final / implemented',
    'https://www.oregon.gov/deq/recycling/Pages/Producers-of-Covered-Products.aspx',

    'REGULATORY_FINAL',

    'CAA was permitted to begin charging producer fees July 1, 2025. Fee rates change annually and depend on producer-reported supply.',

    current_timestamp()
),

(
    'California',
    'SB 54 Plastic Pollution Prevention and Packaging Producer Responsibility Act',
    'CalRecycle',
    'Circular Action Alliance',

    'SB 54 permanent regulations',

    'Implementation active',
    'Future program fee exposure; fee mechanics still implementation-dependent',

    DATE '2026-05-01',
    NULL,

    'Covered material categories under SB 54 include single-use packaging and plastic food service ware, subject to regulatory definitions and exclusions',

    'Final regulations effective',
    'https://calrecycle.ca.gov/packaging/packaging-epr/',

    'REGULATORY_FINAL',

    'Permanent regulations became effective May 1, 2026. Covered-material and recycling-rate determinations are published by CalRecycle; specific producer fee exposure should be modeled only from current approved program data.',

    current_timestamp()
),

(
    'Washington',
    'Recycling Reform Act',
    'Washington State Department of Ecology',
    'Circular Action Alliance',

    'RCW 70A.208 / Recycling Reform Act',

    'Registration obligations beginning',
    'Full service-cost funding later in implementation',

    NULL,
    NULL,

    'Residential consumer packaging and paper products',

    'Law enacted / rulemaking in progress',
    'https://ecology.wa.gov/waste-toxics/reducing-recycling-waste/our-recycling-programs/recycling-reform-act',

    'REGULATORY_IMPLEMENTATION',

    'Washington adopted packaging EPR in 2025. Producer registration and PRO participation begin before full system reimbursement, which starts later in the implementation timeline.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    jurisdiction,
    program_name,
    producer_registration_status,
    producer_fee_status,
    program_effective_date,
    producer_fee_start_date,
    source_status,
    data_classification
FROM kraft_heinz_lca.silver.epr_regulatory_registry
ORDER BY jurisdiction;