# Kraft Heinz Packaging LCA, EPR and FP&A

This is a portfolio case study I built to practice connecting packaging LCA with business decision-making.

The case focuses on a Heinz Tomato Ketchup 20 oz bottle and looks at how packaging changes such as lightweighting and recycled PET could affect:

- packaging carbon footprint
- virgin PET use
- California EPR exposure
- material cost
- annual operating value

The main goal was not just to calculate an LCA result, but to connect the result to procurement, regulatory cost and FP&A.

## What I built

The workflow is:

```text
Public packaging evidence
        ↓
Databricks
        ↓
Packaging BOM and LCI controls
        ↓
openLCA
        ↓
Packaging scenarios
        ↓
California EPR model
        ↓
Procurement and FP&A
        ↓
Power BI
````

I used Databricks for the data pipeline and scenario tables, openLCA for the environmental model, and Power BI for the final decision views.

## Product and functional unit

The case product is Heinz Tomato Ketchup, 20 oz.

Functional unit:

**1 packaged 20 oz ketchup unit**

The current LCA is a screening cradle-to-gate packaging-material model.

It includes:

* PET bottle resin
* recycled PET where used
* PP cap resin
* containerboard proxy

It does not currently include forming, filling, transport, use or end-of-life.

## Scenarios

I modeled four scenarios:

| Scenario | Description                   |
| -------- | ----------------------------- |
| S0       | Baseline                      |
| S1       | 10% bottle lightweighting     |
| S2       | 30% rPET                      |
| S3       | 10% lightweighting + 30% rPET |

These are modeling scenarios for learning and are not Kraft Heinz commitments.

## LCA results

Using TRACI 2.2 in openLCA:

| Scenario | kg CO2e/package | Reduction vs baseline |
| -------- | --------------: | --------------------: |
| S0       |         0.10532 |                     — |
| S1       |         0.09887 |                 6.12% |
| S2       |         0.09357 |                11.16% |
| S3       |         0.08830 |                16.16% |

The PET bottle is the largest modeled hotspot in the baseline.

## California EPR

I modeled California SB 54 separately from the LCA.

This is important because EPR is a regulatory and financial calculation, not an LCIA impact category.

The model estimates fee exposure for the PET bottle, PP cap and corrugated packaging.

Current California fee inputs are illustrative planning values, not final producer fees.

## FP&A connection

I then connected the packaging scenarios to:

* PET material savings
* rPET price premium
* EPR savings
* carbon value sensitivity
* CAPEX sensitivity
* annual operating value

This made the tradeoff between environmental and financial performance much clearer.

For example, lightweighting performs well financially because it reduces material use, while higher rPET content improves environmental performance but can increase procurement cost depending on the assumed resin premium.

## Data governance

One part of the project I focused on was keeping evidence quality visible.

I separated:

* direct product evidence
* contextual company evidence
* external proxies
* synthetic scenario assumptions
* unknown or missing data

I also added controls so contextual evidence could not automatically become an LCI input.

## Repository structure

```text
databricks/
├── 00_project_setup
├── 01_ingestion_and_evidence
├── 02_packaging_and_lci
├── 03_openlca_integration
├── 04_california_epr
├── 05_fpa_and_scenarios
└── 06_powerbi_gold
```

Additional openLCA and Power BI documentation will be added separately.

## Tools

* Databricks
* SQL
* PySpark
* Python
* Delta Lake
* openLCA
* TRACI 2.2
* Power BI
* DAX
* Power Query

## Important note

This is an independent portfolio case study.

It is not an official Kraft Heinz model, product footprint, sales forecast, EPR filing or financial analysis.

Where public product-specific data was not available, I used clearly labeled assumptions or proxies.

## What I learned

The main lesson from this project is that LCA becomes much more useful when it is connected to the decisions people actually need to make.

Instead of stopping at:

> What is the carbon footprint?

the analysis can continue to:

> What is driving the footprint?

> What packaging change reduces it?

> What does that change do to material cost?

> Does it affect EPR exposure?

> What does the business case look like?

That is the direction I wanted to practice with this project.

```
