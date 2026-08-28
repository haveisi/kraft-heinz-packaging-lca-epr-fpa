# Kraft Heinz Packaging LCA, EPR and FP&A

This is a portfolio case study I built to practice connecting packaging life cycle assessment with business decision-making.

The case focuses on a **Heinz Tomato Ketchup 20 oz bottle** and looks at how packaging changes such as lightweighting and recycled PET could affect:

- packaging carbon footprint
- virgin PET use
- recycled PET demand
- California EPR exposure
- material cost
- annual operating value

The main goal was not to stop at a carbon-footprint result. I wanted to connect the environmental model to the kinds of regulatory, procurement, and financial questions that can influence an actual packaging decision.

---

## Project workflow

The project moves from public evidence to environmental modeling and then into business analysis.

```text
Public packaging evidence
        ↓
Databricks Bronze
        ↓
Evidence validation and packaging master
        ↓
Packaging BOM and LCI controls
        ↓
openLCA
        ↓
S0 / S1 / S2 / S3 scenarios
        ↓
California EPR model
        ↓
Procurement and FP&A
        ↓
Databricks Gold
        ↓
Power BI decision model
````

I kept the environmental and financial parts separate where they should be separate.

For example, California EPR fees are not included inside the LCA calculation. They are modeled as a regulatory and financial exposure and then combined with the environmental results later in the decision model.

---

## Product and functional unit

Case product:

**Heinz Tomato Ketchup 20 oz**

Functional unit:

**1 packaged Heinz Tomato Ketchup 20 oz unit**

The current LCA is a screening cradle-to-gate packaging-material model.

It includes:

* virgin PET bottle resin
* recycled PET where used in the scenario
* PP cap resin
* containerboard

It does not currently include:

* label production
* bottle forming
* cap molding
* corrugated converting
* filling
* distribution
* consumer use
* end-of-life

This boundary was chosen so I could first understand the material-production hotspots before expanding the model further.

---

## Standards and methodological references

I used several ISO standards as methodological references while structuring the project.

### ISO 14040

**ISO 14040 — Life cycle assessment: principles and framework**

I used this as the overall structure for thinking about:

* goal and scope
* functional unit
* system boundary
* life cycle inventory
* impact assessment
* interpretation

### ISO 14044

**ISO 14044 — Life cycle assessment: requirements and guidelines**

This was particularly useful for thinking about:

* consistency between the functional unit and inventory
* documenting assumptions
* treatment of missing data and proxies
* interpretation of results
* transparency around limitations

### ISO 14067

**ISO 14067 — Carbon footprint of products**

Because the current comparison focuses on greenhouse gas emissions per packaged unit, ISO 14067 is also relevant to the carbon-footprint side of the project.

I used it as a reference for thinking about:

* product carbon-footprint boundaries
* GHG-focused inventory
* reporting results per functional unit
* transparency around assumptions and exclusions

### ISO 14025

**ISO 14025 — Type III environmental declarations**

I included ISO 14025 mainly as a reference for how LCA results can support more formal environmental product communication.

This project is **not an EPD** and does not claim conformance with a Product Category Rule or EPD program.

### Important standards note

These standards guided the structure and documentation of the case study, but this is still a **screening portfolio analysis**.

It has not undergone external critical review and should not be interpreted as:

* a verified product carbon footprint
* a comparative assertion prepared for public disclosure
* an Environmental Product Declaration
* a fully ISO-conformant corporate product study

---

## Packaging model

The baseline foreground model uses:

| Component          | Modeled amount |
| ------------------ | -------------: |
| Virgin PET bottle  |           30 g |
| PP cap             |            4 g |
| Containerboard     |           18 g |
| Total modeled mass |           52 g |

PET as the bottle material is supported by public Heinz packaging evidence.

Where product-specific public information was not available, I used clearly identified assumptions or proxies rather than treating those values as Kraft Heinz-reported data.

---

## Scenarios

I modeled four scenarios.

| Scenario | Description                           |
| -------- | ------------------------------------- |
| S0       | Baseline                              |
| S1       | 10% PET bottle lightweighting         |
| S2       | 30% recycled PET                      |
| S3       | 10% lightweighting + 30% recycled PET |

These are case-study scenarios for learning and decision analysis.

They are **not Kraft Heinz commitments or announced packaging targets**.

---

## LCA model

I built the environmental model in **openLCA**.

Method:

**TRACI 2.2**

Current impact focus:

**Global Warming Potential**

Result unit:

**kg CO2e per packaged unit**

The openLCA part of the repository includes:

* model configuration
* scenario inputs
* summarized results
* screenshots of model inputs
* screenshots of contribution results

See the [`openlca`](openlca/) folder for the model documentation.

---

## LCA results

The screening results are:

| Scenario          | GWP (kg CO2e/package) | Reduction vs. baseline |
| ----------------- | --------------------: | ---------------------: |
| S0 Baseline       |               0.10532 |                      — |
| S1 Lightweighting |               0.09887 |                  6.12% |
| S2 30% rPET       |               0.09357 |                 11.16% |
| S3 Combined       |               0.08830 |                 16.16% |

The baseline model shows the PET bottle as the largest modeled packaging hotspot.

Approximate baseline contributions are:

* PET bottle: **61%**
* containerboard: **31%**
* PP cap: **8%**

This is why the scenario analysis focuses mainly on bottle lightweighting and recycled PET.

---

## What the scenarios show

### S1 — Lightweighting

The bottle mass is reduced by 10%.

This lowers:

* virgin PET use
* packaging GWP
* modeled EPR exposure
* material demand

Under the financial assumptions used in this case, S1 gives the strongest near-term efficiency case.

### S2 — 30% recycled PET

Part of the virgin PET is replaced with recycled PET.

This lowers:

* virgin PET demand
* modeled GWP

However, the financial result depends strongly on the assumed rPET price premium.

In the current model, S2 is environmentally attractive but financially weaker than lightweighting.

### S3 — Lightweighting + 30% rPET

S3 combines both strategies.

It produces the lowest modeled GWP:

**0.08830 kg CO2e/package**

which is about:

**16.2% below baseline**

It also gives the largest modeled virgin-PET displacement.

---

## Annual scaling

For scenario analysis, I used an assumed California volume of:

**5,000,000 packages per year**

This is a synthetic learning assumption.

It is **not Kraft Heinz sales data**.

At that volume, modeled avoided emissions are approximately:

| Scenario | Annual avoided GHG |
| -------- | -----------------: |
| S1       |        32.25 tCO2e |
| S2       |        58.75 tCO2e |
| S3       |        85.10 tCO2e |

The annual values are useful for connecting the per-package LCA result to procurement and FP&A.

---

## California EPR

I modeled California packaging EPR separately from the environmental LCA.

The current EPR model considers:

* PET bottle
* PP cap
* corrugated packaging

The analysis uses California SB 54 / CAA planning information to estimate potential fee exposure.

Current fee values are treated as:

**illustrative planning inputs**

not final producer invoices.

This distinction is important because the regulatory program is still moving through implementation and fee development.

The EPR model is therefore intended for scenario planning, not compliance filing.

---

## Procurement and FP&A

After building the environmental scenarios, I connected them to several business variables.

The financial model considers:

* virgin PET displacement
* rPET requirement
* PET price sensitivity
* material savings
* EPR cost
* EPR savings
* CAPEX sensitivity
* carbon-value sensitivity
* annual operating value

Public resin-price references are treated as external market proxies.

They are not Kraft Heinz contracted resin prices.

CAPEX and carbon-value cases are also scenario assumptions rather than company-specific inputs.

---

## Environmental and financial tradeoffs

One of the most useful parts of the project was seeing that environmental and financial rankings do not automatically match.

For example:

* **S1 lightweighting** performs well environmentally and financially because less material is required.
* **S2 rPET** improves environmental performance but can increase procurement cost depending on the recycled-resin premium.
* **S3 combined** gives the largest modeled GWP reduction while retaining some of the financial benefit from lightweighting.

This is the main reason I connected LCA with EPR and FP&A instead of treating the LCA as a separate technical exercise.

---

## Data governance

A major part of the project was keeping evidence quality visible.

I separated data into categories such as:

* direct product evidence
* contextual company evidence
* external proxies
* illustrative regulatory inputs
* synthetic scenario assumptions
* unknown or missing data

I also added controls so that contextual evidence could not automatically become a quantitative LCI input.

For example, a public statement about another Kraft Heinz PET bottle can support scenario thinking, but it should not automatically become baseline inventory data for the Heinz 20 oz bottle.

This evidence-governance logic is implemented in the Databricks Silver layer.

---

## Databricks architecture

The analytics pipeline follows a Bronze / Silver / Gold structure.

### Bronze

Used for:

* source registration
* raw evidence
* extracted public information

### Silver

Used for:

* evidence validation
* applicability classification
* packaging master
* LCI registry
* assumptions and proxy controls

### Gold

Used for:

* scenario-ready packaging data
* openLCA results
* EPR calculations
* procurement economics
* FP&A outputs
* Power BI tables

The Databricks notebooks are organized by stage in the [`databricks`](databricks/) folder.

---

## Power BI

The final Power BI report brings together the environmental, regulatory, and financial results.

The main report pages are:

### 1. Packaging Decision Intelligence

Shows:

* avoided GHG
* GWP reduction
* virgin PET displacement
* operating-value range
* environmental versus financial tradeoffs

### 2. LCA & Materials

Shows:

* GWP per package
* scenario comparison
* material mix
* LCA hotspots
* sensitivity analysis

### 3. California EPR & FP&A

Shows:

* illustrative EPR exposure
* EPR savings
* material-cost impact
* procurement sensitivity
* annual operating value

### 4. Data Quality & Assumptions

Documents:

* evidence categories
* assumption status
* fee status
* model boundaries
* data lineage

See the [`powerbi`](powerbi/) folder for screenshots, the semantic model, and selected DAX measures.

---

## Repository structure

```text
databricks/
    data ingestion, evidence governance, LCI controls,
    scenario logic, EPR, FP&A and Gold tables

openlca/
    model configuration, scenario inputs,
    results and openLCA screenshots

powerbi/
    report screenshots, semantic model
    and selected DAX measures
```

---

## Main data quality controls

Some of the controls I added during the project include:

* one evidence record per evidence ID
* direct versus analogous evidence classification
* explicit proxy flags
* LCI eligibility checks
* scenario classification
* openLCA result reconciliation
* one-row-per-scenario Power BI grain
* controlled scenario relationships in the semantic model

The final Power BI decision source passed a basic grain check of:

**4 rows / 4 distinct scenarios**

for S0 through S3.

---

## Tools

I used:

* Databricks
* SQL
* Python
* PySpark
* Delta Lake
* openLCA
* USLCI / Federal LCA Commons reference data
* TRACI 2.2
* Power BI
* DAX
* Power Query
* Excel

---

## What I learned

The main lesson from this project is that packaging LCA becomes much more useful when it is connected to the decisions that follow the footprint calculation.

Instead of stopping at:

> What is the packaging carbon footprint?

I wanted the workflow to continue into questions such as:

> Which material is driving the result?

> What happens if the bottle is lightweighted?

> What happens if recycled content increases?

> How does the material change affect California EPR exposure?

> What happens to procurement cost?

> Which option provides the strongest overall business case?

That connection between environmental analysis and business decision-making is the main reason I built the project this way.

---

## Limitations

This project is an independent screening case study.

Important limitations include:

* some component masses are assumptions or proxies
* California annual volume is synthetic
* resin prices are external market proxies
* California EPR fee values are illustrative
* CAPEX and carbon values are scenario assumptions
* bottle forming and other conversion processes are currently excluded
* distribution and end-of-life are outside the current LCA boundary
* no external critical review has been completed

The results should not be interpreted as Kraft Heinz corporate data, an official product footprint, an EPR filing, or a financial forecast.

```
