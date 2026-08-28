# openLCA model

This folder contains the openLCA part of my packaging case study for a Heinz Tomato Ketchup 20 oz bottle.

I used openLCA to compare a baseline package with lightweighting and recycled PET scenarios. The main purpose was to understand how changes in the bottle design affect packaging-related greenhouse gas emissions before connecting those results to the EPR and financial parts of the project.

## What I modeled

The functional unit is:

**1 packaged Heinz Tomato Ketchup 20 oz unit**

The current model is a screening cradle-to-gate packaging-material assessment.

The model includes:

- virgin PET resin
- recycled PET resin where applicable
- PP cap resin
- containerboard

The current model does not include bottle forming, cap molding, filling, distribution, use, or end-of-life.

I used **TRACI 2.2** and focused on global warming potential.

## Scenarios

I modeled four scenarios:

| Scenario | Description |
|---|---|
| S0 | Baseline |
| S1 | 10% PET bottle lightweighting |
| S2 | 30% recycled PET |
| S3 | 10% lightweighting + 30% recycled PET |

These are modeling scenarios for this case study and are not Kraft Heinz commitments.

## Main results

| Scenario | GWP, kg CO2e/package | Reduction vs. baseline |
|---|---:|---:|
| S0 | 0.10532 | — |
| S1 | 0.09887 | 6.12% |
| S2 | 0.09357 | 11.16% |
| S3 | 0.08830 | 16.16% |

The baseline result shows PET as the largest modeled packaging hotspot. The combined S3 scenario gives the largest reduction in this screening model.

## Files in this folder

- `model_configuration.md` — model setup, system boundary and LCI references
- `scenario_inputs.csv` — material inputs for S0-S3
- `results_summary.csv` — modeled GWP results
- `screenshots/` — selected openLCA inputs and result views

## Screenshots

### Baseline inputs

The baseline foreground process uses 30 g virgin PET, 4 g PP and 18 g containerboard.

![Baseline inputs](screenshots/01_baseline_s0_inputs.png)

### Combined lightweighting + rPET inputs

In S3, the bottle mass is reduced and part of the PET is replaced with recycled PET.

![S3 inputs](screenshots/02_combined_s3_inputs.png)

### Baseline GWP result

![Baseline GWP overview](screenshots/03_baseline_s0_gwp_overview.png)

The contribution view shows the baseline total and the main material contributions.

![Baseline GWP contributions](screenshots/04_baseline_s0_gwp_contributions.png)

### Combined scenario result

![S3 GWP overview](screenshots/05_combined_s3_gwp_overview.png)

The S3 contribution view shows how the mix changes after lightweighting and rPET are introduced.

![S3 GWP contributions](screenshots/06_combined_s3_gwp_contributions.png)

## Important note

This is a screening model for learning and portfolio use.

Some packaging masses and material choices are based on documented assumptions or proxies where product-specific public data was not available. The model has not undergone external critical review and should not be interpreted as an official Kraft Heinz product footprint.
