-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.lci_data_gap_matrix (
    gap_id STRING,

    target_product STRING,
    lci_stage STRING,
    lci_field STRING,
    packaging_component STRING,

    required_unit STRING,
    required_for_model BOOLEAN,

    evidence_status STRING,
    evidence_id STRING,

    current_value DOUBLE,
    current_value_text STRING,
    current_unit STRING,

    value_origin STRING,

    source_strength STRING,
    direct_applicability BOOLEAN,

    modeling_action STRING,
    gap_priority STRING,

    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.lci_data_gap_matrix

VALUES

(
    'GAP-001',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'primary_container_material',
    'bottle',
    NULL,
    TRUE,
    'Direct evidence available',
    'KH20-001',
    NULL,
    'PET',
    NULL,
    'reported',
    'High',
    TRUE,
    'Use in baseline LCI',
    'Closed',
    'Direct Kraft Heinz evidence supports PET bottle material.',
    current_timestamp()
),

(
    'GAP-002',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'primary_container_structure',
    'bottle',
    NULL,
    TRUE,
    'Direct evidence available',
    'KH20-002',
    NULL,
    'single-layer',
    NULL,
    'reported',
    'High',
    TRUE,
    'Use in baseline LCI',
    'Closed',
    'Direct Kraft Heinz evidence supports single-layer structure.',
    current_timestamp()
),

(
    'GAP-003',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'bottle_mass',
    'bottle',
    'g',
    TRUE,
    'Assumption only',
    NULL,
    30,
    '30 g training assumption',
    'g',
    'assumption',
    'Low',
    FALSE,
    'Replace with measured, supplier-specific, or defensible secondary-source value',
    'Critical',
    'Existing training workbook uses 30 g. This is not Kraft Heinz-reported data.',
    current_timestamp()
),

(
    'GAP-004',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'bottle_recycled_content',
    'bottle',
    '%',
    TRUE,
    'Analogous evidence only',
    'KH25-002',
    NULL,
    '100% recycled PET applies to other Kraft Heinz bottles',
    '%',
    'proxy',
    'Medium',
    FALSE,
    'Baseline must not use 100% rPET. Use only in an explicitly labeled scenario unless direct ketchup evidence is found.',
    'High',
    'Kraft Mayo, Miracle Whip and NotMayo evidence is analogous, not direct.',
    current_timestamp()
),

(
    'GAP-005',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'closure_material',
    'cap',
    NULL,
    TRUE,
    'Missing direct evidence',
    NULL,
    NULL,
    NULL,
    NULL,
    'unknown',
    'None',
    FALSE,
    'Find product specification, packaging source, measurement, or defensible proxy',
    'High',
    'Do not assume PP merely because PP caps are common.',
    current_timestamp()
),

(
    'GAP-006',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'closure_mass',
    'cap',
    'g',
    TRUE,
    'Assumption only',
    NULL,
    4,
    '4 g training assumption',
    'g',
    'assumption',
    'Low',
    FALSE,
    'Replace with measurement or supplier/product data',
    'High',
    'Existing workbook value is illustrative.',
    current_timestamp()
),

(
    'GAP-007',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'label_material',
    'label',
    NULL,
    TRUE,
    'Missing direct evidence',
    NULL,
    NULL,
    NULL,
    NULL,
    'unknown',
    'None',
    FALSE,
    'Find packaging specification or inspect physical product',
    'Medium',
    'Label composition has not been established.',
    current_timestamp()
),

(
    'GAP-008',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'label_mass',
    'label',
    'g',
    TRUE,
    'Assumption only',
    NULL,
    1,
    '1 g training assumption',
    'g',
    'assumption',
    'Low',
    FALSE,
    'Replace with measurement or supplier/product data',
    'Medium',
    'Existing workbook value is illustrative.',
    current_timestamp()
),

(
    'GAP-009',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'secondary_packaging_material',
    'corrugated_case',
    NULL,
    TRUE,
    'Assumption only',
    NULL,
    NULL,
    'corrugated board',
    NULL,
    'assumption',
    'Low',
    FALSE,
    'Confirm shipper configuration and material',
    'Medium',
    'Training model assumes corrugated secondary packaging.',
    current_timestamp()
),

(
    'GAP-010',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A1 Material production',
    'secondary_packaging_allocation_mass',
    'corrugated_case',
    'g/FU',
    TRUE,
    'Assumption only',
    NULL,
    18,
    '18 g per 20 oz bottle',
    'g/FU',
    'assumption',
    'Low',
    FALSE,
    'Confirm case weight and bottles per case',
    'High',
    'Allocation must be based on actual case configuration.',
    current_timestamp()
),

(
    'GAP-011',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A2 Transport',
    'supplier_transport_distance',
    'bottle',
    'km',
    TRUE,
    'Assumption only',
    NULL,
    500,
    '500 km training assumption',
    'km',
    'assumption',
    'Low',
    FALSE,
    'Replace with supplier/manufacturing geography or scenario distance',
    'High',
    'Distance is illustrative.',
    current_timestamp()
),

(
    'GAP-012',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A2 Transport',
    'transport_mode',
    'bottle',
    NULL,
    TRUE,
    'Assumption only',
    NULL,
    NULL,
    'truck',
    NULL,
    'assumption',
    'Low',
    FALSE,
    'Confirm logistics mode',
    'Medium',
    'Truck is a screening assumption.',
    current_timestamp()
),

(
    'GAP-013',
    'Heinz Tomato Ketchup 20 oz bottle',
    'A3 Conversion',
    'packaging_conversion_energy',
    'bottle',
    'kWh/FU',
    TRUE,
    'Missing',
    NULL,
    NULL,
    NULL,
    NULL,
    'unknown',
    'None',
    FALSE,
    'Find supplier/process data or use transparent secondary proxy',
    'High',
    'No direct conversion-energy evidence currently available.',
    current_timestamp()
),

(
    'GAP-014',
    'Heinz Tomato Ketchup 20 oz bottle',
    'End of life',
    'recycling_rate',
    'bottle',
    '%',
    TRUE,
    'Missing product-specific value',
    NULL,
    NULL,
    NULL,
    '%',
    'secondary_data_needed',
    'None',
    FALSE,
    'Use geography-specific public recycling data',
    'High',
    'Design recyclability is not the same as actual recycling rate.',
    current_timestamp()
),

(
    'GAP-015',
    'Heinz Tomato Ketchup 20 oz bottle',
    'End of life',
    'landfill_rate',
    'bottle',
    '%',
    TRUE,
    'Missing product-specific value',
    NULL,
    NULL,
    NULL,
    '%',
    'secondary_data_needed',
    'None',
    FALSE,
    'Derive from geography-specific end-of-life scenario',
    'High',
    'Must be consistent with recycling/incineration assumptions.',
    current_timestamp()
),

(
    'GAP-016',
    'Heinz Tomato Ketchup 20 oz bottle',
    'Impact factor',
    'PET_emission_factor',
    'PET',
    'kg CO2e/kg',
    TRUE,
    'Training factor only',
    NULL,
    3.0,
    '3.0 kg CO2e/kg PET',
    'kg CO2e/kg',
    'proxy',
    'Low',
    FALSE,
    'Replace with documented LCA database/process dataset',
    'Critical',
    'Training factor is not decision-grade.',
    current_timestamp()
);

-- COMMAND ----------

SELECT
    gap_id,
    lci_stage,
    lci_field,
    current_value_text,
    evidence_status,
    source_strength,
    modeling_action,
    gap_priority
FROM kraft_heinz_lca.silver.lci_data_gap_matrix
ORDER BY gap_id;

-- COMMAND ----------

SELECT
    gap_id,
    lci_stage,
    lci_field,
    current_value_text,
    evidence_status,
    source_strength,
    modeling_action,
    gap_priority
FROM kraft_heinz_lca.silver.lci_data_gap_matrix
ORDER BY gap_id;

-- COMMAND ----------

SELECT
    evidence_status,
    COUNT(*) AS number_of_fields
FROM kraft_heinz_lca.silver.lci_data_gap_matrix
GROUP BY evidence_status
ORDER BY number_of_fields DESC;

-- COMMAND ----------

SELECT
    COUNT(*) AS required_fields,

    SUM(
        CASE
            WHEN gap_priority = 'Closed'
            THEN 1
            ELSE 0
        END
    ) AS closed_fields,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN gap_priority = 'Closed'
                THEN 1
                ELSE 0
            END
        )
        /
        COUNT(*),
        1
    ) AS direct_evidence_readiness_pct

FROM kraft_heinz_lca.silver.lci_data_gap_matrix
WHERE required_for_model = TRUE;