-- Databricks notebook source
CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.ca_sb54_cmc_reference (
    cmc_id STRING,

    material_class STRING,
    material_type STRING,
    form STRING,

    recyclable_flag BOOLEAN,
    compostable_flag BOOLEAN,

    recycling_rate_pct DOUBLE,

    source_version STRING,
    source_date DATE,
    source_url STRING,

    regulatory_status STRING,
    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.ca_sb54_cmc_reference
VALUES

(
    '25_P1P',
    'Plastic',
    'PET (#1)',
    'Bottles, Jugs, and Jars (Clear/Natural)',
    TRUE,
    FALSE,
    16.0,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Candidate CMC for a clear/natural PET ketchup bottle. Exact Heinz bottle color/marking still requires verification.',
    current_timestamp()
),

(
    '25_P2P',
    'Plastic',
    'PET (#1)',
    'Bottles, Jugs, and Jars (Pigmented/Color)',
    TRUE,
    FALSE,
    5.0,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Candidate CMC if the PET bottle itself is pigmented or colored.',
    current_timestamp()
),

(
    '25_PF9N',
    'Paper and Fiber',
    'OCC',
    'Cardboard w/o plastic component',
    TRUE,
    TRUE,
    68.0,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Candidate CMC for corrugated shipping case if no plastic component is present.',
    current_timestamp()
),

(
    '25_PF9P',
    'Paper and Fiber',
    'OCC',
    'Cardboard w/ plastic component',
    TRUE,
    FALSE,
    68.0,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Candidate CMC if corrugated packaging contains a plastic component.',
    current_timestamp()
);

-- COMMAND ----------

SELECT *
FROM kraft_heinz_lca.silver.ca_sb54_cmc_reference
ORDER BY cmc_id;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.packaging_cmc_mapping (
    sku_id STRING,
    component_id STRING,
    packaging_component STRING,

    material_type STRING,
    packaging_form STRING,

    candidate_cmc_id STRING,
    final_cmc_id STRING,

    classification_status STRING,
    confidence_status STRING,

    evidence_status STRING,
    regulatory_source STRING,

    reviewer_note STRING,

    updated_timestamp TIMESTAMP
)
USING DELTA;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.packaging_cmc_mapping
VALUES

(
    'SKU-KH-20OZ',
    'COMP-BOTTLE',
    'Bottle',

    'PET',
    'Bottle',

    '25_P1P OR 25_P2P',
    NULL,

    'PROVISIONAL',
    'MEDIUM',

    'PET and bottle form are direct evidence; color classification still unverified.',

    'CalRecycle SB 54 CMC List January 2026',

    'Do not finalize CMC until PET bottle clear/natural versus pigmented/color status is verified.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'COMP-CAP',
    'Cap',

    NULL,
    'Closure / lid',

    NULL,
    NULL,

    'BLOCKED',
    'LOW',

    'Cap material is currently unknown.',

    'CalRecycle SB 54 CMC List January 2026',

    'Cannot assign SB 54 material category until cap polymer/material is established.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'COMP-LABEL',
    'Label',

    NULL,
    'Label',

    NULL,
    NULL,

    'BLOCKED',
    'LOW',

    'Label material is currently unknown.',

    'CalRecycle SB 54 CMC List January 2026',

    'Cannot assign SB 54 CMC until label material and construction are established.',

    current_timestamp()
),

(
    'SKU-KH-20OZ',
    'COMP-CASE',
    'Corrugated case allocation',

    'Corrugated board',
    'Cardboard',

    '25_PF9N OR 25_PF9P',
    NULL,

    'PROVISIONAL',
    'MEDIUM',

    'Corrugated board is currently a training assumption; plastic-component status is unknown.',

    'CalRecycle SB 54 CMC List January 2026',

    'Use 25_PF9N only after confirming the case has no plastic component; otherwise evaluate 25_PF9P.',

    current_timestamp()
);

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    candidate_cmc_id,
    final_cmc_id,
    classification_status,
    confidence_status,
    evidence_status
FROM kraft_heinz_lca.silver.packaging_cmc_mapping
ORDER BY component_id;

-- COMMAND ----------

SELECT *
FROM kraft_heinz_lca.silver.packaging_cmc_mapping
WHERE final_cmc_id IS NOT NULL
  AND classification_status <> 'FINAL';

-- COMMAND ----------

SELECT *
FROM kraft_heinz_lca.silver.packaging_cmc_mapping
WHERE classification_status = 'FINAL'
  AND final_cmc_id IS NULL;

-- COMMAND ----------

SELECT
    component_id,
    packaging_component,
    material_type,
    evidence_id,
    evidence_status,
    value_origin,
    data_quality_status
FROM kraft_heinz_lca.gold.packaging_master
ORDER BY component_id;

-- COMMAND ----------

UPDATE kraft_heinz_lca.gold.packaging_master
SET
    material_family = 'Plastic',
    material_type = 'PET',
    evidence_status = 'Verified PET; clear/natural bottle form supported by Heinz 20 oz packaging evidence',
    value_origin = 'VERIFIED-DIRECT',
    data_quality_status = 'High',
    reviewer_note = 'Heinz 20 oz packaging evidence identifies a clear PETE #1 bottle. Current Kraft Heinz ESG evidence independently supports single-layer PET ketchup bottles. Bottle mass remains a separate assumption.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-BOTTLE';

-- COMMAND ----------

UPDATE kraft_heinz_lca.gold.packaging_master
SET
    material_family = 'Plastic',
    material_type = 'PP',
    evidence_status = 'Verified current Heinz mono-material ketchup cap design; exact California 20 oz SKU rollout not directly confirmed',
    value_origin = 'VERIFIED-PROXY',
    data_quality_status = 'Medium-High',
    reviewer_note = 'Kraft Heinz confirms the redesigned recyclable ketchup cap uses a single rigid material; supplier and technical evidence identifies the material as polypropylene. Exact 2026 California 20 oz SKU applicability remains to be confirmed. Cap mass remains a training assumption.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-CAP';

-- COMMAND ----------

UPDATE kraft_heinz_lca.gold.packaging_master
SET
    material_family = 'Plastic',
    material_type = 'PP',
    evidence_status = 'Verified current Heinz mono-material ketchup cap design; exact California 20 oz SKU rollout not directly confirmed',
    value_origin = 'VERIFIED-PROXY',
    data_quality_status = 'Medium-High',
    reviewer_note = 'Kraft Heinz confirms the redesigned recyclable ketchup cap uses a single rigid material; supplier and technical evidence identifies the material as polypropylene. Exact 2026 California 20 oz SKU applicability remains to be confirmed. Cap mass remains a training assumption.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-CAP';

-- COMMAND ----------

UPDATE kraft_heinz_lca.silver.packaging_cmc_mapping
SET
    material_type = 'PET',
    packaging_form = 'Bottles, Jugs, and Jars (Clear/Natural)',
    candidate_cmc_id = '25_P1P',
    final_cmc_id = '25_P1P',
    classification_status = 'FINAL',
    confidence_status = 'HIGH',
    evidence_status = 'PET and clear bottle form supported by Heinz 20 oz packaging evidence.',
    reviewer_note = 'Finalized as clear/natural PET bottle under current SB 54 CMC structure. Bottle mass remains an independent modeling assumption.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-BOTTLE';

-- COMMAND ----------

UPDATE kraft_heinz_lca.silver.packaging_cmc_mapping
SET
    material_type = 'PP',
    packaging_form = 'Closure / cap',
    classification_status = 'PROVISIONAL',
    confidence_status = 'MEDIUM-HIGH',
    evidence_status = 'PP supported by current Heinz mono-material cap design evidence; exact California 20 oz SKU applicability not directly confirmed.',
    reviewer_note = 'Material gap substantially closed. Next step is to map PP closure form to the exact current CalRecycle CMC before finalizing.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-CAP';

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    candidate_cmc_id,
    final_cmc_id,
    classification_status,
    confidence_status
FROM kraft_heinz_lca.silver.packaging_cmc_mapping
ORDER BY component_id;

-- COMMAND ----------

INSERT INTO kraft_heinz_lca.silver.ca_sb54_cmc_reference
VALUES

(
    '25_P41P',
    'Plastic',
    'PP (#5)',
    'Other Rigid Containers, Cups, Lids, Plates, Trays, Tubs',
    TRUE,
    FALSE,
    2.0,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Candidate category for a polypropylene ketchup cap/lid if it does not fall under the SB 54 small-format category.',
    current_timestamp()
),

(
    '25_P47P',
    'Plastic',
    'Plastic',
    'Small – Two or more sides measuring 2 inches or less',
    FALSE,
    FALSE,
    NULL,
    'SB 54 Covered Material Category List January 2026',
    DATE '2025-12-31',
    'https://www2.calrecycle.ca.gov/Docs/Publications/137815',
    'REGULATORY_FINAL',
    'Potential category if the ketchup cap meets CalRecycle small-format dimensional criteria. Recycling rate listed as insufficient information.',
    current_timestamp()
);

-- COMMAND ----------

SELECT
    cmc_id,
    material_type,
    form,
    recyclable_flag,
    recycling_rate_pct
FROM kraft_heinz_lca.silver.ca_sb54_cmc_reference
WHERE cmc_id IN ('25_P41P', '25_P47P');

-- COMMAND ----------

UPDATE kraft_heinz_lca.silver.packaging_cmc_mapping
SET
    material_type = 'PP',
    packaging_form = 'Closure / lid',
    candidate_cmc_id = '25_P41P OR 25_P47P',
    final_cmc_id = NULL,
    classification_status = 'PROVISIONAL',
    confidence_status = 'MEDIUM',
    evidence_status = 'PP material supported; exact small-format dimensional classification not yet verified.',
    reviewer_note = 'Current SB 54 candidates are 25_P41P for PP lids or 25_P47P if the cap meets the small-format rule of two or more sides measuring 2 inches or less. Do not finalize until dimensions are verified.',
    updated_timestamp = current_timestamp()
WHERE sku_id = 'SKU-KH-20OZ'
  AND component_id = 'COMP-CAP';

-- COMMAND ----------

SELECT
    packaging_component,
    material_type,
    packaging_form,
    candidate_cmc_id,
    final_cmc_id,
    classification_status,
    confidence_status
FROM kraft_heinz_lca.silver.packaging_cmc_mapping
WHERE component_id = 'COMP-CAP';