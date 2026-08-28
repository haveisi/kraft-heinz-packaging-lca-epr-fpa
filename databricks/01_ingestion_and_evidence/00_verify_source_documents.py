# Databricks notebook source
SOURCE_PATH = "/Volumes/kraft_heinz_lca/bronze/source_documents/"

files = dbutils.fs.ls(SOURCE_PATH)

for f in files:
    print(
        f"name={f.name} | "
        f"size_bytes={f.size} | "
        f"path={f.path}"
    )

# COMMAND ----------

expected_files = {
    "KraftHeinz-2025-ESG-Report.pdf",
    "KraftHeinz_2024-ESG-Report.pdf",
    "Kraft_Heinz_Packaging_LCA_Learning_Workbook.xlsx",
    "source_manifest.txt"
}

actual_files = {f.name for f in dbutils.fs.ls(SOURCE_PATH)}

missing_files = expected_files - actual_files
unexpected_files = actual_files - expected_files

print("Expected:", expected_files)
print("Actual:", actual_files)
print("Missing:", missing_files)
print("Unexpected:", unexpected_files)

if not missing_files:
    print("SOURCE DOCUMENT CHECK: PASS")
else:
    print("SOURCE DOCUMENT CHECK: FAIL")

# COMMAND ----------

