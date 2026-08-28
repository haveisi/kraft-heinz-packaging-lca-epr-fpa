# Kraft Heinz Packaging LCA, EPR and FP&A

This is a portfolio case study I built to practice connecting packaging LCA with business decision-making.

The case focuses on a Heinz Tomato Ketchup 20 oz bottle and looks at how packaging changes such as lightweighting and recycled PET could affect:

- packaging carbon footprint
- virgin PET use
- California EPR exposure
- material cost
- annual operating value

The goal was not to stop at a carbon-footprint result. I wanted to connect the environmental results to procurement, regulatory cost and FP&A.

## Project workflow

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

## Product and functional unit

Case product:

**Heinz Tomato Ketchup 20 oz**

Functional unit:

**1 packaged 20 oz ketchup unit**

The current LCA is a screening cradle-to-gate packaging-material model.

It includes:

* PET bottle resin
* recycled PET where used
* PP cap resin
* containerboard

It does not currently include forming, filling, transport, use, or end-of-life.

## Scenarios

I modeled four scenarios:

| Scenario | Description                   |
| -------- | ----------------------------- |
| S0       | Baseline                      |
| S1       | 10% bottle lightweighting     |
| S2       | 30% rPET                      |
| S3       | 10% lightweighting + 30% rPET |

These are case-study scenarios and are not Kraft Heinz commitments.

## LCA results

Using TRACI 2.2 in openLCA:

| Scenario | kg CO2e/package | Reduction vs. baseline |
| -------- | --------------: | ---------------------: |
| S0       |         0.10532 |                      — |
| S1       |         0.09887 |                  6.12% |
| S2       |         0.09357 |                 11.16% |
| S3       |         0.08830 |                 16.16% |

The PET bottle is the largest modeled hotspot in the baseline.

## California EPR and FP&A

I modeled California EPR separately from the LCA because EPR is a regulatory and financial calculation rather than an LCIA impact.

The scenario analysis then connects:

* material reduction
* rPET price sensitivity
* EPR exposure
* procurement impact
* operating value
* CAPEX and carbon-value sensitivity

This makes it easier to compare environmental and financial tradeoffs across the scenarios.

## Repository structure

```text
databricks/
    data ingestion, evidence controls, scenario logic and Gold tables

openlca/
    LCA model setup, scenario inputs, results and screenshots

powerbi/
    Power BI report documentation, semantic model, DAX measures and screenshots
```

## Power BI report

The report has three main decision pages:

1. Packaging Decision Intelligence
2. LCA & Materials
3. California EPR & FP&A

A fourth page documents data quality and assumptions.

See the `powerbi/` folder for screenshots and model documentation.

## Data and assumptions

I separated:

* direct public evidence
* contextual company evidence
* external proxies
* illustrative regulatory inputs
* synthetic scenario assumptions

This was important because I did not want contextual information to silently become LCI or financial data.

## Tools

* Databricks
* SQL
* Python / PySpark
* Delta Lake
* openLCA
* TRACI 2.2
* Power BI
* DAX
* Power Query

## Important note

This is an independent portfolio case study.

It is not an official Kraft Heinz LCA, EPR filing, sales forecast, or financial analysis.

Where product-specific public data was not available, I used clearly labeled assumptions or proxies.
