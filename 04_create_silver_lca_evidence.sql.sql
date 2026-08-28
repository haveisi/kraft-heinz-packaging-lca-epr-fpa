-- Databricks notebook source
CREATE SCHEMA IF NOT EXISTS kraft_heinz_lca.silver;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.lca_evidence (
    silver_id STRING,

    evidence_id STRING,

    target_product STRING,
    target_brand STRING,

    evidence_category STRING,
    evidence_subcategory STRING,

    source_product STRING,
    source_brand STRING,

    packaging_component STRING,
    material STRING,

    extracted_value DOUBLE,
    extracted_value_text STRING,
    extracted_unit STRING,

    reporting_year INT,
    geography STRING,

    applicability_status STRING,
    applicability_reason STRING,

    evidence_strength STRING,
    lca_usability STRING,

    value_origin STRING,

    requires_assumption BOOLEAN,
    assumption_description STRING,

    source_document STRING,
    source_page INT,

    bronze_review_status STRING,

    silver_review_status STRING,
    silver_reviewer_note STRING,

    silver_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.lca_evidence

SELECT
    CONCAT('S-', evidence_id) AS silver_id,

    evidence_id,

    'Heinz Tomato Ketchup 20 oz bottle' AS target_product,
    'Heinz' AS target_brand,

    evidence_category,
    evidence_subcategory,

    product_name AS source_product,
    brand AS source_brand,

    packaging_component,
    material,

    extracted_value,
    extracted_value_text,
    extracted_unit,

    reporting_year,
    geography,

    CASE

        WHEN product_name = 'Heinz Tomato Ketchup 20 oz bottle'
            THEN 'Direct'

        WHEN evidence_id IN ('KH25-001','KH25-002','KH25-003')
            THEN 'Analogous'

        WHEN evidence_id IN (
            'KH25-004',
            'KH25-005',
            'KH25-006',
            'KH25-007',
            'KH25-008',
            'KH25-009'
        )
            THEN 'Contextual'

        ELSE 'Needs Assessment'

    END AS applicability_status,

    CASE

        WHEN product_name = 'Heinz Tomato Ketchup 20 oz bottle'
            THEN 'Evidence explicitly applies to target product.'

        WHEN evidence_id IN ('KH25-001','KH25-002','KH25-003')
            THEN 'Evidence applies to other Kraft Heinz PET bottle products and may support a labeled recycled-PET scenario, but not the baseline Heinz ketchup inventory.'

        WHEN evidence_id IN ('KH25-004','KH25-005')
            THEN 'Different product and packaging format; useful as evidence of packaging lightweighting/material reduction strategy.'

        WHEN evidence_id IN ('KH25-006','KH25-007')
            THEN 'Different Heinz packaging format; useful for design-for-recycling discussion but not target-product LCI.'

        WHEN evidence_id IN ('KH25-008','KH25-009')
            THEN 'Different dispensing system; useful for reuse/single-use avoidance scenario concepts but not target-product LCI.'

        ELSE 'Applicability not yet assessed.'

    END AS applicability_reason,

    CASE
        WHEN review_status = 'Approved'
             AND ai_confidence >= 0.90
            THEN 'High'
        WHEN review_status = 'Approved'
            THEN 'Medium'
        ELSE 'Low'
    END AS evidence_strength,

    CASE

        WHEN product_name = 'Heinz Tomato Ketchup 20 oz bottle'
             AND review_status = 'Approved'
            THEN 'LCI Candidate'

        WHEN evidence_id IN ('KH25-001','KH25-002','KH25-003')
            THEN 'Scenario Evidence'

        ELSE 'Interpretation Only'

    END AS lca_usability,

    value_origin,

    CASE
        WHEN product_name <> 'Heinz Tomato Ketchup 20 oz bottle'
        THEN TRUE
        ELSE FALSE
    END AS requires_assumption,

    CASE
        WHEN evidence_id IN ('KH25-001','KH25-002','KH25-003')
        THEN 'Using this evidence for Heinz ketchup requires an explicit cross-product proxy assumption.'

        WHEN product_name <> 'Heinz Tomato Ketchup 20 oz bottle'
        THEN 'Evidence relates to a different product or packaging system and must not be transferred directly.'

        ELSE NULL
    END AS assumption_description,

    source_document,
    source_page,

    review_status AS bronze_review_status,

    'Needs Review' AS silver_review_status,

    'Initial rule-based Silver classification; requires review before Gold promotion.' AS silver_reviewer_note,

    current_timestamp()

FROM kraft_heinz_lca.bronze.report_evidence

WHERE review_status = 'Approved';

-- COMMAND ----------

SELECT
    silver_id,
    evidence_id,
    source_product,
    evidence_category,
    material,
    applicability_status,
    evidence_strength,
    lca_usability,
    requires_assumption

FROM kraft_heinz_lca.silver.lca_evidence

ORDER BY evidence_id;

-- COMMAND ----------

SELECT
    silver_id,
    evidence_id,
    source_product,
    target_product,
    applicability_status

FROM kraft_heinz_lca.silver.lca_evidence

WHERE applicability_status = 'Direct'
  AND source_product <> target_product;

-- COMMAND ----------

SELECT
    silver_id,
    evidence_id,
    applicability_status,
    lca_usability,
    requires_assumption,
    silver_review_status

FROM kraft_heinz_lca.silver.lca_evidence

WHERE lca_usability = 'LCI Candidate'
  AND (
       applicability_status <> 'Direct'
       OR requires_assumption = TRUE
       OR silver_review_status <> 'Approved'
  );

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC SOURCE_PATH = "/Volumes/kraft_heinz_lca/bronze/source_documents/"
-- MAGIC
-- MAGIC for f in dbutils.fs.ls(SOURCE_PATH):
-- MAGIC     print(f.name)
-- MAGIC

-- COMMAND ----------

SELECT
    path,
    length,
    modificationTime
FROM read_files(
    '/Volumes/kraft_heinz_lca/bronze/source_documents/',
    format => 'binaryFile',
    fileNamePattern => '*.pdf'
)
WHERE _metadata.file_name = 'KraftHeinz-ESG-Report-2020.pdf';

-- COMMAND ----------

SELECT
    path AS source_path,

    ai_parse_document(
        content,
        map(
            'version', '2.0',
            'pageRange', '30-34'
        )
    ) AS parsed_document

FROM read_files(
    '/Volumes/kraft_heinz_lca/bronze/source_documents/',
    format => 'binaryFile'
)

WHERE _metadata.file_name = 'KraftHeinz-ESG-Report-2020.pdf';

-- COMMAND ----------

WITH parsed AS (

    SELECT
        path AS source_path,

        ai_parse_document(
            content,
            map(
                'version', '2.0',
                'pageRange', '30-34'
            )
        ) AS doc

    FROM read_files(
        '/Volumes/kraft_heinz_lca/bronze/source_documents/',
        format => 'binaryFile'
    )

    WHERE _metadata.file_name = 'KraftHeinz-ESG-Report-2020.pdf'
)

SELECT
    source_path,

    ai_extract(
        doc,

        '{
          "ketchup_packaging_evidence": {
            "type": "array",
            "description": "Extract only packaging evidence explicitly applying to Heinz Ketchup bottles.",
            "items": {
              "type": "object",
              "properties": {

                "product": {
                  "type": "string",
                  "description": "Exact Heinz ketchup product or bottle group explicitly described."
                },

                "packaging_component": {
                  "type": "string",
                  "description": "Packaging component explicitly mentioned."
                },

                "material": {
                  "type": "string",
                  "description": "Packaging material explicitly stated. Do not infer polymers not named."
                },

                "structure": {
                  "type": "string",
                  "description": "Explicit packaging structure such as single-layer or multilayer."
                },

                "size_scope": {
                  "type": "string",
                  "description": "Any explicit product-size applicability or exclusion."
                },

                "implementation_year": {
                  "type": "string",
                  "description": "Year explicitly associated with implementation."
                },

                "recyclability_statement": {
                  "type": "string",
                  "description": "Explicit recycling or recyclability claim."
                },

                "reported_quantity": {
                  "type": "string",
                  "description": "Quantitative number of bottles or other packaging quantity explicitly reported."
                },

                "evidence_text": {
                  "type": "string",
                  "description": "Concise source-grounded description without unsupported inference."
                }

              }
            }
          }
        }',

        options => map(
            'version', '2.1',
            'mode', 'precision',
            'enableCitations', 'true',
            'enableConfidenceScores', 'true',
            'instructions',
            'Extract only statements explicitly about Heinz Ketchup bottle packaging. Do not infer bottle mass, recycled content, cap material, label material, transport distance, or emission factors. Preserve product-size exclusions exactly.'
        )
    ) AS extraction

FROM parsed;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.bronze.evidence_categories VALUES
('packaging_scope', 'Product size, format, or applicability boundaries'),
('implementation_timing', 'Implementation start, completion, or transition timing'),
('reported_quantity', 'Reported physical quantity associated with a packaging initiative');

-- COMMAND ----------

SELECT *
FROM kraft_heinz_lca.bronze.evidence_categories
ORDER BY evidence_category;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.bronze.report_evidence
(
    evidence_id,
    source_document,
    source_path,
    source_type,
    source_page,
    source_section,
    raw_text,
    evidence_category,
    evidence_subcategory,
    product_name,
    brand,
    packaging_component,
    material,
    extracted_value,
    extracted_value_text,
    extracted_unit,
    reporting_year,
    geography,
    value_origin,
    extraction_method,
    ai_confidence,
    review_status,
    reviewer_note,
    extraction_timestamp
)

VALUES

-- 1. PET material
(
    'KH20-001',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'Heinz began converting its plastic ketchup bottles to a single layer of PET plastic in 2017; by the end of 2018, all Heinz Ketchup bottles, excluding those larger than 64 ounces, were reformatted to a single-layer design, making them easier to recycle.',

    'packaging_material',
    'primary_container_material',

    'Heinz Ketchup bottles <=64 oz',
    'Heinz',
    'bottle',
    'PET',

    NULL,
    'PET plastic',
    NULL,

    2018,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'Direct product-family evidence. The target 20 oz Heinz ketchup bottle falls within the explicitly reported <=64 oz scope.',

    current_timestamp()
),

-- 2. Single-layer structure
(
    'KH20-002',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'Heinz began converting its plastic ketchup bottles to a single layer of PET plastic in 2017; by the end of 2018, all Heinz Ketchup bottles, excluding those larger than 64 ounces, were reformatted to a single-layer design, making them easier to recycle.',

    'packaging_material',
    'single_layer_structure',

    'Heinz Ketchup bottles <=64 oz',
    'Heinz',
    'bottle',
    'PET',

    NULL,
    'single-layer',
    NULL,

    2018,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'Direct evidence that applicable Heinz ketchup bottles use a single-layer bottle structure.',

    current_timestamp()
),

-- 3. Size applicability
(
    'KH20-003',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'By the end of 2018, all Heinz Ketchup bottles excluding those larger than 64 ounces were reformatted to a single-layer design.',

    'packaging_scope',
    'size_scope',

    'Heinz Ketchup bottles <=64 oz',
    'Heinz',
    'bottle',
    'PET',

    64,
    'excluding those larger than 64 ounces',
    'oz',

    2018,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'This boundary establishes direct applicability to the 20 oz target bottle.',

    current_timestamp()
),

-- 4. Recyclability
(
    'KH20-004',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'The single-layer design made Heinz ketchup bottles easier to recycle.',

    'recyclability',
    'design_for_recycling',

    'Heinz Ketchup bottles <=64 oz',
    'Heinz',
    'bottle',
    'PET',

    NULL,
    'easier to recycle',
    NULL,

    2018,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'Qualitative recyclability evidence only. It must not be converted into a recycling rate or percentage.',

    current_timestamp()
),

-- 5. Transition start
(
    'KH20-005',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'Heinz began converting its plastic ketchup bottles to a single layer of PET plastic in 2017.',

    'implementation_timing',
    'conversion_start',

    'Heinz Ketchup bottles',
    'Heinz',
    'bottle',
    'PET',

    2017,
    'conversion began in 2017',
    'year',

    2017,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'Preserves the implementation start separately from completion.',

    current_timestamp()
),

-- 6. Bottles converted
(
    'KH20-006',
    'KraftHeinz-ESG-Report-2020.pdf',
    '/Volumes/kraft_heinz_lca/bronze/source_documents/KraftHeinz-ESG-Report-2020.pdf',
    'ESG Report',
    32,
    'Packaging / Heinz Ketchup Bottle Redesign',

    'Between 2017 and 2019, 290 million bottles were converted from essentially non-recyclable to more readily recyclable.',

    'reported_quantity',
    'bottles_converted',

    'Heinz Ketchup bottles',
    'Heinz',
    'bottle',
    'PET',

    290,
    '290 million bottles',
    'million bottles',

    2019,
    NULL,

    'reported',
    'AI_extracted_human_validated',

    0.95,
    'Approved',

    'Reported aggregate transition quantity for 2017-2019. Do not interpret as annual production or as quantity of 20 oz bottles specifically.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    evidence_id,
    evidence_category,
    evidence_subcategory,
    product_name,
    packaging_component,
    material,
    extracted_value,
    extracted_value_text,
    extracted_unit,
    reporting_year,
    review_status
FROM kraft_heinz_lca.bronze.report_evidence
WHERE evidence_id LIKE 'KH20-%'
ORDER BY evidence_id;

-- COMMAND ----------

SELECT COUNT(*) AS total_bronze_rows
FROM kraft_heinz_lca.bronze.report_evidence;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.lca_evidence

SELECT
    CONCAT('S-', evidence_id),

    evidence_id,

    'Heinz Tomato Ketchup 20 oz bottle',
    'Heinz',

    evidence_category,
    evidence_subcategory,

    product_name,
    brand,

    packaging_component,
    material,

    extracted_value,
    extracted_value_text,
    extracted_unit,

    reporting_year,
    geography,

    'Direct',

    'The source applies to Heinz ketchup bottles excluding sizes greater than 64 oz; the target product is 20 oz and is therefore inside the reported applicability boundary.',

    'High',

    CASE
        WHEN evidence_id IN ('KH20-001','KH20-002')
            THEN 'LCI Candidate'

        WHEN evidence_id = 'KH20-003'
            THEN 'Applicability Evidence'

        WHEN evidence_id = 'KH20-004'
            THEN 'Interpretation Evidence'

        WHEN evidence_id IN ('KH20-005','KH20-006')
            THEN 'Supporting Evidence'

        ELSE 'Needs Assessment'
    END,

    value_origin,

    FALSE,

    NULL,

    source_document,
    source_page,

    review_status,

    'Approved',

    CASE

        WHEN evidence_id = 'KH20-001'
        THEN 'Approved as direct evidence that the target ketchup bottle primary container is PET.'

        WHEN evidence_id = 'KH20-002'
        THEN 'Approved as direct evidence for a single-layer bottle structure.'

        WHEN evidence_id = 'KH20-003'
        THEN 'Approved as applicability evidence confirming that 20 oz falls within the reported <=64 oz scope.'

        WHEN evidence_id = 'KH20-004'
        THEN 'Approved for qualitative recyclability interpretation; not a quantitative EoL input.'

        WHEN evidence_id = 'KH20-005'
        THEN 'Approved as historical implementation timing.'

        WHEN evidence_id = 'KH20-006'
        THEN 'Approved as aggregate historical transition evidence; not an activity quantity for the target functional unit.'

    END,

    current_timestamp()

FROM kraft_heinz_lca.bronze.report_evidence

WHERE evidence_id LIKE 'KH20-%'
  AND review_status = 'Approved';

-- COMMAND ----------

SELECT
    evidence_id,
    source_product,
    material,
    applicability_status,
    evidence_strength,
    lca_usability,
    requires_assumption,
    silver_review_status
FROM kraft_heinz_lca.silver.lca_evidence
WHERE evidence_id LIKE 'KH20-%'
ORDER BY evidence_id;

-- COMMAND ----------

SELECT COUNT(*) AS silver_rows
FROM kraft_heinz_lca.silver.lca_evidence;

-- COMMAND ----------

SELECT COUNT(*) AS direct_lci_candidates
FROM kraft_heinz_lca.silver.lca_evidence
WHERE applicability_status = 'Direct'
  AND lca_usability = 'LCI Candidate'
  AND silver_review_status = 'Approved';