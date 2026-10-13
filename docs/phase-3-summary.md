# Phase 3 — Synthetic Operational Dataset

## Objective

Build a deterministic synthetic enterprise dataset that supports the documented OpsIntel BI business, reporting, data-modeling, validation, and data-quality requirements.

## Completed Datasets

The generator now produces the following clean reference datasets:

```text
data/generated/
├── regions.csv
├── locations.csv
├── customers.csv
├── carriers.csv
├── routes.csv
├── assets.csv
├── shipments.csv
├── transportation_costs.csv
├── transportation_budgets.csv
├── asset_movements.csv
├── operational_exceptions.csv
└── data_quality_issues.csv
```

The project also produces source-like datasets containing controlled defects:

```text
data/raw/
├── shipments.csv
└── transportation_costs.csv
```

## Dataset Scale

Current configured scale:

```text
Regions                     3
Locations                  80
Customers                 300
Carriers                   20
Routes                    300
Assets                  5,000
Shipments              100,000
Transportation Budgets     99
```

Transportation costs, asset movements, and operational exceptions contain variable row counts based on generated business behavior.

The reporting period is:

```text
2024-01-01 through 2026-09-30
```

This represents 33 calendar months.

## Business Behavior

The synthetic generator intentionally creates analytical patterns rather than purely random records.

Examples include:

- carrier service profiles influence on-time performance
- carrier service profiles influence transportation cost
- route distance affects transportation cost
- transportation mode affects cost behavior
- shipment quantity affects transportation cost
- seasonal patterns affect transportation budgets
- late deliveries create operational exceptions
- cancelled shipments create operational exceptions
- unusually high shipment costs create cost anomalies
- asset movements create operational history

## Carrier Profiles

Carrier profiles currently include:

```text
PREMIUM
STANDARD
ECONOMY
```

These profiles influence:

- transportation cost
- expected service performance
- transit behavior

The purpose is to create realistic cost-versus-service trade-offs for later BI analysis.

## Data Quality Strategy

Clean reference datasets are retained under:

```text
data/generated/
```

Controlled source-like defects are written to:

```text
data/raw/
```

Injected defects include:

- duplicate shipment records
- missing carrier references
- invalid delivery dates
- invalid shipment quantities
- extreme transportation-cost anomalies

A generated manifest records the known injected defects:

```text
data/generated/data_quality_issues.csv
```

This enables later comparison between:

```text
known injected defect
        ↓
SQL detection
        ↓
staging treatment
        ↓
clean analytical model
```

## Validation

Automated tests are located under:

```text
tests/
├── test_generated_data.py
└── test_reproducibility.py
```

The validation suite covers:

- record counts
- uniqueness
- referential integrity
- required-field behavior
- geographic consistency
- shipment logic
- transportation-cost logic
- budget grain
- asset-movement integrity
- exception integrity
- raw-source defect presence
- deterministic generation

## Reproducibility

Synthetic data generation uses:

```text
RANDOM_SEED = 42
```

Reproducibility is validated using SHA-256 file hashes across repeated generator executions.

The intended reproducibility contract is:

```text
same code
+ same configuration
+ same random seed
+ same dependency versions
= same generated datasets
```

Exact Python dependencies are captured in:

```text
requirements-lock.txt
```

## Architecture Boundary

Phase 3 establishes a clear boundary for Phase 4:

```text
Synthetic Generator
        ↓
data/raw/
        ↓
PostgreSQL raw schema
        ↓
SQL validation and cleaning
        ↓
staging schema
        ↓
dimensional analytical model
```

Clean generated datasets remain available as reference truth for validation.

## Phase 3 Outcome

OpsIntel BI now has a deterministic, validated, source-like operational dataset suitable for database ingestion, data-quality processing, dimensional modeling, SQL validation, and Power BI development.

The project is ready to proceed to:

**Phase 4 — PostgreSQL Foundation**