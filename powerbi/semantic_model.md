# Power BI semantic model

The report uses a simple star-style model.

`DimScenario` is the main shared dimension.

Relationships:

- DimScenario -> FactPackagingScenario
- DimScenario -> FactLCAComponent
- DimScenario -> FactScenarioMaterial
- DimScenario -> FactEPRScenario
- DimScenario -> FactProcurementScenario

All relationships are one-to-many and single-direction.

I avoided direct fact-to-fact relationships because they created ambiguous filter paths during development.

The final Power BI source table was rebuilt at a controlled grain of one row per scenario.

QA result:

- row count: 4
- distinct scenarios: 4
- status: PASS