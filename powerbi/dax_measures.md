# DAX measures

These are the main measures I used in the Power BI report.

## Scenario selection

```DAX
Selected Scenario =
SELECTEDVALUE(
    DimScenario[scenario_name],
    "All Scenarios"
)
````

## Environmental measures

```DAX
Annual Avoided GHG =
SUM(
    FactPackagingScenario[annual_avoided_gwp_tco2e]
)
```

```DAX
GWP Reduction % =
DIVIDE(
    MAX(FactPackagingScenario[gwp_reduction_pct]),
    100
)
```

```DAX
GWP per Package =
MAX(
    FactPackagingScenario[gwp_kg_co2e_per_package]
)
```

```DAX
GWP per Package gCO2e =
[GWP per Package] * 1000
```

```DAX
Virgin PET Displaced =
SUM(
    FactPackagingScenario[annual_virgin_pet_displacement_kg]
)
```

```DAX
Source Reduction =
SUM(
    FactPackagingScenario[annual_plastic_source_reduction_kg]
)
```

```DAX
rPET Requirement =
SUM(
    FactPackagingScenario[annual_rpet_kg]
)
```

## Financial measures

```DAX
Operating Value - Min =
SUM(
    FactPackagingScenario[annual_operating_value_min_usd]
)
```

```DAX
Operating Value - Max =
SUM(
    FactPackagingScenario[annual_operating_value_max_usd]
)
```

```DAX
Operating Value Midpoint =
DIVIDE(
    [Operating Value - Min]
        + [Operating Value - Max],
    2
)
```

```DAX
Operating Value Range =
[Operating Value - Max]
    - [Operating Value - Min]
```

```DAX
Operating Value per tCO2e =
DIVIDE(
    [Operating Value Midpoint],
    [Annual Avoided GHG]
)
```

## California EPR measures

```DAX
EPR Cost - Low =
SUM(
    FactEPRScenario[total_epr_low_usd]
)
```

```DAX
EPR Cost - High =
SUM(
    FactEPRScenario[total_epr_high_usd]
)
```

```DAX
EPR Savings - Low =
SUM(
    FactEPRScenario[annual_epr_savings_low_usd]
)
```

```DAX
EPR Savings - High =
SUM(
    FactEPRScenario[annual_epr_savings_high_usd]
)
```

```DAX
EPR Cost Midpoint =
DIVIDE(
    [EPR Cost - Low]
        + [EPR Cost - High],
    2
)
```

```DAX
EPR Savings Midpoint =
DIVIDE(
    [EPR Savings - Low]
        + [EPR Savings - High],
    2
)
```

## Procurement measures

```DAX
Material Savings - Low =
SUM(
    FactProcurementScenario[material_savings_low_usd]
)
```

```DAX
Material Savings - High =
SUM(
    FactProcurementScenario[material_savings_high_usd]
)
```

```DAX
Material Savings Midpoint =
DIVIDE(
    [Material Savings - Low]
        + [Material Savings - High],
    2
)
```

## LCA contribution measures

```DAX
Base Component GWP gCO2e =
SUM(
    FactLCAComponent[impact_result]
) * 1000
```

```DAX
Component Contribution % =
DIVIDE(
    SUM(FactLCAComponent[impact_result]),
    CALCULATE(
        SUM(FactLCAComponent[impact_result]),
        ALLEXCEPT(
            FactLCAComponent,
            FactLCAComponent[scenario_id]
        )
    )
)
```

## Sensitivity measures

```DAX
Selected Bottle Mass Factor =
SELECTEDVALUE(
    LCASensitivity[BottleMassFactor],
    1
)
```

```DAX
Selected rPET Factor =
SELECTEDVALUE(
    LCASensitivity[rPETShareFactor],
    1
)
```

```DAX
Selected Board Factor =
SELECTEDVALUE(
    LCASensitivity[BoardFactor],
    1
)
```

```DAX
Sensitivity Adjusted Component GWP =
VAR Component =
    SELECTEDVALUE(
        FactLCAComponent[Component Display]
    )

VAR BaseImpact =
    [Base Component GWP gCO2e]

VAR Factor =
    SWITCH(
        Component,
        "PET Bottle", [Selected Bottle Mass Factor],
        "rPET", [Selected rPET Factor],
        "Containerboard Case", [Selected Board Factor],
        "PP Cap", 1,
        1
    )

RETURN
    BaseImpact * Factor
```

## Decision interpretation

```DAX
Selected Decision Category =
SELECTEDVALUE(
    FactPackagingScenario[decision_category],
    "No scenario selected"
)
```

These measures support the environmental, EPR, procurement and financial views in the report.

```
