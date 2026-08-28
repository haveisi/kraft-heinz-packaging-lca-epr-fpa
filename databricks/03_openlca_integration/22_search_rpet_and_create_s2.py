# Databricks notebook source
import json
import zipfile
import pandas as pd

zip_path = "/Volumes/kraft_heinz_lca/bronze/lca_reference_data/uslci_pet_jsonld.zip"

rpet_matches = []

with zipfile.ZipFile(zip_path, "r") as z:
    for name in z.namelist():

        if "/processes/" not in name or not name.endswith(".json"):
            continue

        try:
            with z.open(name) as f:
                data = json.load(f)

            process_name = data.get("name", "")
            name_lower = process_name.lower()

            # Much broader PET recycling search
            if (
                "terephthalate" in name_lower
                or "pet" in name_lower
            ) and (
                "recycl" in name_lower
                or "postconsumer" in name_lower
                or "post-consumer" in name_lower
                or "flake" in name_lower
                or "pellet" in name_lower
            ):

                qref = next(
                    (
                        e for e in data.get("exchanges", [])
                        if e.get("isQuantitativeReference") is True
                    ),
                    None
                )

                location = data.get("location")

                if isinstance(location, dict):
                    location_name = location.get("name")
                else:
                    location_name = None

                rpet_matches.append({
                    "process_id": data.get("@id"),
                    "process_name": process_name,
                    "location": location_name,
                    "reference_flow": (
                        qref.get("flow", {}).get("name")
                        if qref else None
                    ),
                    "reference_amount": (
                        qref.get("amount")
                        if qref else None
                    ),
                    "reference_unit": (
                        qref.get("unit", {}).get("name")
                        if qref else None
                    )
                })

print("Matches found:", len(rpet_matches))

# COMMAND ----------

pet_names = []

with zipfile.ZipFile(zip_path, "r") as z:
    for name in z.namelist():

        if "/processes/" not in name or not name.endswith(".json"):
            continue

        try:
            with z.open(name) as f:
                data = json.load(f)

            process_name = data.get("name", "")

            if (
                "pet" in process_name.lower()
                or "terephthalate" in process_name.lower()
            ):
                pet_names.append({
                    "process_id": data.get("@id"),
                    "process_name": process_name
                })

        except Exception:
            pass

pet_names_df = pd.DataFrame(pet_names)

print("PET-related processes:", len(pet_names_df))

display(
    pet_names_df.sort_values("process_name")
)