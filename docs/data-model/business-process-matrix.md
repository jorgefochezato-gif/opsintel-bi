# Business Process Matrix

## Purpose

This document maps the major business processes in OpsIntel BI to the dimensions that will be used to analyze them.

The matrix helps define which facts and dimensions are required before implementing the dimensional model.

## Business Processes

The initial analytical solution will model these primary business processes:

1. Shipments
2. Transportation Costs
3. Asset Movements
4. Budget
5. Operational Exceptions

Each process may become one or more fact tables depending on its analytical grain.

---

## Candidate Dimensions

The initial shared dimensions are:

- Date
- Customer
- Carrier
- Location
- Region
- Asset
- Route

Additional dimensions may be introduced if required by later business rules.

---

## Bus Matrix

| Business Process | Date | Customer | Carrier | Location | Region | Asset | Route |
|---|---|---|---|---|---|---|---|
| Shipments | X | X | X | X | X |  | X |
| Transportation Costs | X | X | X | X | X |  | X |
| Asset Movements | X |  |  | X | X | X |  |
| Budget | X |  |  |  | X |  |  |
| Operational Exceptions | X | X | X | X | X | X | X |

The exact dimensional relationships will be refined during detailed modeling.

---

## Business Process: Shipments

### Description

Represents the movement of goods or reusable logistics assets from an origin location to a destination location.

### Candidate Fact Table

```text
FactShipment
```

### Initial Grain

One row per shipment.

This means every row should represent exactly one unique shipment.

### Candidate Measures

- Shipment Count
- Shipment Volume
- Transit Time
- Late Shipment Count
- On-Time Shipment Count

### Candidate Dimensions

- Shipment Date
- Expected Delivery Date
- Actual Delivery Date
- Customer
- Carrier
- Origin Location
- Destination Location
- Region
- Route

### Design Consideration

Multiple date relationships will likely exist.

For example:

```text
Shipment Date
Expected Delivery Date
Actual Delivery Date
```

The model will need to determine which Date relationship is active by default and how alternate date contexts will be handled.

---

## Business Process: Transportation Costs

### Description

Represents transportation-related costs incurred while moving shipments.

### Candidate Fact Table

```text
FactTransportationCost
```

### Initial Grain

One row per transportation cost transaction.

A shipment may therefore have one or multiple transportation cost records.

### Candidate Measures

- Total Transportation Cost
- Cost per Shipment
- Carrier Cost per Shipment
- Budget Variance
- Budget Variance Percentage

### Candidate Dimensions

- Cost Date
- Shipment
- Customer
- Carrier
- Region
- Location
- Route
- Cost Type

### Design Consideration

Transportation cost records must not be duplicated when joined to shipment-level information.

The relationship between shipment grain and cost-transaction grain will therefore need careful modeling.

---

## Business Process: Asset Movements

### Description

Represents the movement and status changes of reusable logistics assets across the operational network.

### Candidate Fact Table

```text
FactAssetMovement
```

### Initial Grain

One row per asset movement event.

### Candidate Measures

- Asset Movement Count
- Active Asset Count
- Available Asset Count
- Asset Utilization Percentage

### Candidate Dimensions

- Movement Date
- Asset
- Origin Location
- Destination Location
- Region
- Movement Type
- Asset Status

### Design Consideration

Asset utilization is a semi-additive or snapshot-style analytical problem and may require a dedicated periodic snapshot fact table later.

---

## Business Process: Budget

### Description

Represents planned transportation spending.

### Candidate Fact Table

```text
FactTransportationBudget
```

### Initial Grain

One row per region per month.

Example:

```text
2026-01 | North America | 1,250,000
2026-01 | Europe        |   950,000
2026-01 | Latin America |   475,000
```

### Candidate Measures

- Transportation Budget
- Budget Variance
- Budget Variance Percentage

### Candidate Dimensions

- Date
- Region

### Design Consideration

Actual transportation cost will exist at a more detailed grain than budget.

Comparisons must aggregate actual cost to the compatible region/month grain before meaningful variance analysis.

---

## Business Process: Operational Exceptions

### Description

Represents events that require operational attention.

Examples:

- delivery delay
- missing asset
- shipment cancellation
- cost anomaly
- route exception
- damaged asset

### Candidate Fact Table

```text
FactOperationalException
```

### Initial Grain

One row per operational exception event.

### Candidate Measures

- Exception Count
- Exception Rate
- Exceptions by Type
- Exceptions by Region
- Exceptions by Carrier

### Candidate Dimensions

- Exception Date
- Customer
- Carrier
- Location
- Region
- Asset
- Route
- Exception Type
- Severity

---

# Conformed Dimensions

A conformed dimension is a dimension shared consistently across multiple business processes.

OpsIntel BI is expected to use conformed dimensions such as:

```text
DimDate
DimCustomer
DimCarrier
DimLocation
DimRegion
DimAsset
DimRoute
```

For example, the same `DimCarrier` should support both:

```text
FactShipment
```

and:

```text
FactTransportationCost
```

This allows users to compare shipment performance and transportation cost using the same carrier definitions.

---

# Why Grain Matters

The grain defines exactly what one row in a fact table represents.

Examples:

```text
FactShipment
    One row = one shipment

FactTransportationCost
    One row = one transportation cost transaction

FactAssetMovement
    One row = one asset movement event

FactTransportationBudget
    One row = one region per month
```

Fact tables with different grain should not be combined carelessly.

Doing so can cause:

- duplicated values
- incorrect totals
- misleading averages
- incorrect DAX calculations

The grain must therefore be explicitly documented before table implementation.

---

# Open Modeling Questions

The following questions will be resolved during detailed dimensional modeling:

- Can one shipment use multiple carriers?
- Can one shipment have multiple delivery attempts?
- Can a shipment contain multiple asset types?
- Should origin and destination use role-playing Location dimensions?
- Should transportation cost types have their own dimension?
- Should exceptions be modeled as a separate fact table or as shipment attributes?
- Is asset utilization better represented through movements or periodic snapshots?
- How should cancelled shipments be represented?
- How should partial deliveries be represented?
- How should routes be uniquely identified?
- Should Region exist independently or be derived from Location?