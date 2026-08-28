-- Databricks notebook source
SELECT
    flow_type,
    is_input,
    is_quantitative_reference,
    COUNT(*) AS n
FROM kraft_heinz_lca.silver.lca_process_exchanges
GROUP BY
    flow_type,
    is_input,
    is_quantitative_reference
ORDER BY
    flow_type,
    is_input;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS kraft_heinz_lca.silver.lca_process_exchanges_classified AS

SELECT
    *,

    CASE

        WHEN is_quantitative_reference = TRUE
            THEN 'REFERENCE_PRODUCT'

        WHEN flow_type = 'PRODUCT_FLOW'
             AND is_input = TRUE
            THEN 'TECHNOSPHERE_INPUT'

        WHEN flow_type = 'PRODUCT_FLOW'
             AND is_input = FALSE
            THEN 'TECHNOSPHERE_OUTPUT'

        WHEN flow_type = 'ELEMENTARY_FLOW'
             AND is_input = TRUE
            THEN 'ELEMENTARY_INPUT'

        WHEN flow_type = 'ELEMENTARY_FLOW'
             AND is_input = FALSE
            THEN 'ELEMENTARY_OUTPUT'

        ELSE 'REVIEW'

    END AS exchange_class

FROM kraft_heinz_lca.silver.lca_process_exchanges
WHERE dataset_id = 'DATA-PET-001';

-- COMMAND ----------

SELECT
    exchange_class,
    COUNT(*) AS exchange_count
FROM kraft_heinz_lca.silver.lca_process_exchanges_classified
GROUP BY exchange_class
ORDER BY exchange_class;

-- COMMAND ----------

SELECT
    flow_name,
    amount,
    unit,
    exchange_class
FROM kraft_heinz_lca.silver.lca_process_exchanges_classified
WHERE exchange_class = 'REFERENCE_PRODUCT';

-- COMMAND ----------

SELECT
    flow_name,
    amount,
    unit,
    flow_type
FROM kraft_heinz_lca.silver.lca_process_exchanges_classified
WHERE exchange_class = 'TECHNOSPHERE_INPUT'
ORDER BY ABS(amount) DESC
LIMIT 20;

-- COMMAND ----------

SELECT
    flow_name,
    amount,
    unit
FROM kraft_heinz_lca.silver.lca_process_exchanges_classified
WHERE exchange_class = 'ELEMENTARY_OUTPUT'
ORDER BY ABS(amount) DESC
LIMIT 20;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC import json
-- MAGIC
-- MAGIC PET_JSON = (
-- MAGIC     "/Volumes/kraft_heinz_lca/bronze/lca_reference_data/"
-- MAGIC     "uslci_pet_virgin_resin_at_plant.json"
-- MAGIC )
-- MAGIC
-- MAGIC with open(PET_JSON, "r", encoding="utf-8") as f:
-- MAGIC     pet_raw = json.load(f)
-- MAGIC
-- MAGIC exchanges = pet_raw.get("exchanges", [])
-- MAGIC
-- MAGIC with_provider = [
-- MAGIC     ex for ex in exchanges
-- MAGIC     if ex.get("provider") is not None
-- MAGIC ]
-- MAGIC
-- MAGIC print("Total exchanges:", len(exchanges))
-- MAGIC print("Exchanges with provider:", len(with_provider))
-- MAGIC
-- MAGIC if with_provider:
-- MAGIC     print("\nFirst exchange with provider:")
-- MAGIC     print(with_provider[0])