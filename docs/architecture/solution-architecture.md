# Solution Architecture

## Purpose

This document defines the initial high-level architecture for OpsIntel BI.

The architecture separates data generation, storage, transformation, analytical modeling, visualization, security, and validation into distinct layers so that each responsibility can be understood, tested, and evolved independently.

## High-Level Architecture

```text
Synthetic Data Generation
        |
        v
Generated Source Files
        |
        v
PostgreSQL
        |
        v
Raw / Staging Layer
        |
        v
SQL Transformation Layer
        |
        v
Dimensional Analytics Model
        |
        v
Power BI Semantic Model
        |
        v
DAX Measures
        |
        v
Row-Level Security
        |
        v
Interactive Reports
        |
        v
Business Insights
```

Validation operates across multiple layers:

```text
Source Data
    |
    v
PostgreSQL
    |
    v
SQL Validation Queries
    |
    +----------------------+
                           |
                           v
                    Power BI Measures
                           |
                           v
                    Report Validation
```

## Architecture Layers

### 1. Synthetic Data Generation

Purpose:

- Generate realistic enterprise operational data.
- Control dataset size and business rules.
- Introduce realistic data-quality conditions.
- Make the project reproducible.

Primary technology:

- Python

Expected outputs:

- customers
- carriers
- locations
- assets
- shipments
- asset movements
- transportation costs
- budgets
- operational exceptions

Generated files will initially be stored under:

```text
data/generated/
```

---

### 2. Database Layer

Purpose:

- Store operational and analytical data.
- Enforce structural integrity.
- Support SQL transformations and validation.
- Provide the primary data source for Power BI.

Primary technology:

- PostgreSQL

Runtime environment:

- Docker

The database will eventually contain multiple logical layers such as:

```text
raw
staging
analytics
```

The exact schema design will be finalized during later phases.

---

### 3. Raw Layer

Purpose:

- Preserve source-like data with minimal transformation.
- Provide traceability between generated source data and downstream models.
- Allow data-quality problems to remain observable.

Examples:

```text
raw.customers
raw.shipments
raw.transportation_costs
raw.asset_movements
```

The raw layer should avoid unnecessary business logic.

---

### 4. Staging Layer

Purpose:

- Clean and standardize source data.
- Resolve data types.
- Handle invalid or missing values.
- Remove or flag duplicates.
- Prepare source data for analytical modeling.

Examples:

```text
staging.customers_clean
staging.shipments_clean
staging.transportation_costs_clean
```

The staging layer represents validated and standardized operational data, but not yet the final dimensional model.

---

### 5. SQL Transformation Layer

Purpose:

- Apply explicit business transformation logic.
- Build analytical structures from standardized data.
- Keep transformation logic visible and testable.
- Support reconciliation with Power BI.

Primary technology:

- SQL

Repository location:

```text
sql/transformations/
```

Validation queries will be stored separately under:

```text
sql/validation/
```

---

### 6. Dimensional Analytics Layer

Purpose:

- Organize data for analytical workloads.
- Create reusable facts and dimensions.
- Support predictable filtering and aggregation.
- Provide a clean source for the Power BI semantic model.

Expected dimensional structure:

```text
FactShipment
FactTransportationCost
FactAssetMovement

DimDate
DimCustomer
DimCarrier
DimLocation
DimRegion
DimAsset
DimRoute
```

The exact fact table grain and relationships will be defined during the dimensional-modeling phase.

The preferred design pattern is a star schema.

---

### 7. Power BI Semantic Model

Purpose:

- Represent business relationships and analytical logic.
- Provide reusable measures and dimensions.
- Hide unnecessary implementation details from report consumers.
- Support consistent reporting across multiple pages.

Expected responsibilities:

- table relationships
- measure organization
- display folders
- business-friendly field names
- hidden technical columns
- date relationships
- reusable calculations
- security integration

Power BI should consume the analytical model rather than reproduce extensive transformation logic that belongs in SQL.

---

### 8. DAX Calculation Layer

Purpose:

- Implement analytical calculations that depend on report filter context.
- Provide reusable business measures.
- Support time intelligence and comparative analysis.

Examples:

```text
Total Transportation Cost
Shipment Count
Cost per Shipment
On-Time Delivery %
YTD Transportation Cost
Previous-Year Transportation Cost
YoY Cost Change %
Budget Variance %
```

DAX calculations should be validated against independent SQL queries whenever practical.

---

### 9. Security Layer

Purpose:

- Restrict report data according to user responsibilities.
- Demonstrate enterprise-grade access control.

Initial concept:

```text
Executive
    -> All Regions

Regional Manager
    -> Assigned Region

Operations Manager
    -> Assigned Operational Area
```

Power BI Row-Level Security will be used to implement the final security model.

---

### 10. Reporting Layer

Purpose:

- Present analytical information in a decision-oriented format.
- Support executive monitoring and operational investigation.

Expected report areas:

```text
Executive Overview
Regional Operations
Carrier Performance
Customer / Route Analysis
Operational Exceptions
```

Every visualization should answer a documented business question.

---

### 11. Validation Layer

Validation is treated as a first-class architectural responsibility.

Validation will include:

- source record counts
- duplicate detection
- referential-integrity checks
- SQL aggregation checks
- SQL-to-DAX reconciliation
- filter behavior testing
- Row-Level Security testing
- dashboard functional testing

The objective is not merely to display plausible numbers.

The objective is to demonstrate that reported numbers can be independently reproduced and trusted.

## Separation of Responsibilities

The project will generally follow this principle:

```text
Python
    -> Generate realistic source data

PostgreSQL
    -> Store and organize data

SQL
    -> Clean, transform, model, and validate data

Power BI Semantic Model
    -> Define analytical relationships

DAX
    -> Perform context-dependent analytical calculations

Power BI Reports
    -> Communicate insights and support decisions
```

This separation is intended to improve:

- maintainability
- testability
- transparency
- performance
- reusability

## Data Flow

The intended data flow is:

```text
Python Generator
      |
      v
CSV / Generated Files
      |
      v
PostgreSQL Raw Tables
      |
      v
Staging Tables
      |
      v
Dimensional Tables
      |
      v
Power BI
      |
      v
Semantic Model
      |
      v
DAX Measures
      |
      v
Reports
```

## Guiding Architecture Principles

1. Business definitions should exist before calculations.
2. Transformation logic should live in the most appropriate layer.
3. SQL and DAX responsibilities should remain clearly separated.
4. Power BI should consume a clean analytical model.
5. Dimensional models should favor predictable star-schema relationships.
6. Metrics should be reproducible outside the visualization layer.
7. Security should be designed rather than added as an afterthought.
8. Raw data should remain traceable.
9. Important design decisions should be documented.
10. The architecture should remain understandable to another engineer or analyst reviewing the repository.