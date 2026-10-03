# Business Rules and Edge Cases

## Purpose

This document defines the business rules that govern how operational records should be interpreted before they are transformed into analytical metrics.

The goal is to make important assumptions explicit so that SQL transformations, DAX measures, validation queries, and report behavior remain consistent.

# Shipment Status Rules

The initial shipment statuses are:

```text
PLANNED
IN_TRANSIT
DELIVERED
CANCELLED
```

Only completed shipments should be included in delivery-performance metrics.

For the initial implementation:

```text
Completed Shipment = DELIVERED
```

Cancelled shipments must not be included in:

- On-Time Delivery Percentage
- Late Shipment Rate
- Average Transit Time

Cancelled shipments may still be included in operational exception analysis.

# On-Time Delivery Rule

A delivered shipment is considered on time when:

```text
Actual Delivery Date <= Expected Delivery Date
```

A delivered shipment is considered late when:

```text
Actual Delivery Date > Expected Delivery Date
```

If a delivered shipment is missing either:

- Expected Delivery Date
- Actual Delivery Date

then it should not be included in on-time or late-delivery calculations.

The missing-date condition should be flagged as a data-quality issue.

# Transit Time Rule

Transit time is calculated only for delivered shipments with valid shipment and delivery dates.

```text
Transit Time Days
=
Actual Delivery Date - Shipment Date
```

The calculation must not produce a negative result.

If:

```text
Actual Delivery Date < Shipment Date
```

the record should be treated as invalid and flagged for data-quality review.

# Shipment Count Rule

Shipment Count represents the number of distinct shipment identifiers.

```text
Shipment Count
=
COUNT DISTINCT Shipment ID
```

Duplicate source rows must not artificially increase shipment count.

# Shipment Volume Rule

Shipment Volume represents the total quantity transported.

```text
Shipment Volume
=
SUM(Shipment Quantity)
```

Shipment quantity must be greater than zero for valid shipment records.

Zero or negative shipment quantities should be flagged as invalid.

# Transportation Cost Rules

Transportation cost records may occur multiple times for the same shipment.

For example:

```text
Shipment 1001
    Base Freight
    Fuel Surcharge
    Accessorial Charge
```

Therefore:

```text
One shipment != one transportation cost record
```

Total Transportation Cost should include all valid cost records associated with the selected reporting context.

Cost records must not be duplicated through joins to shipment-level or dimensional tables.

# Transportation Cost Validation

Valid transportation cost values should normally be:

```text
Cost Amount >= 0
```

Negative transportation costs may represent:

- credits
- corrections
- reversals

Negative values should not automatically be removed.

They should instead include an identifiable cost type or transaction type explaining the negative amount.

Unexpected negative values should be flagged for validation.

# Cost per Shipment Rule

```text
Cost per Shipment
=
Total Transportation Cost
/
Distinct Shipment Count
```

The denominator should represent shipments associated with the applicable transportation cost context.

If Shipment Count is zero, the result should be blank.

# Budget Rules

Budget will initially exist at:

```text
Month + Region
```

grain.

Budget should therefore not be interpreted at customer, carrier, shipment, or route level unless a future allocation methodology is explicitly introduced.

Example:

```text
January 2026
North America
Transportation Budget = 1,250,000
```

Actual transportation costs may be much more granular but must be aggregated to a compatible reporting context for variance calculations.

# Budget Variance Rule

```text
Budget Variance
=
Actual Transportation Cost
-
Budget Transportation Cost
```

Interpretation:

```text
Positive variance = above budget
Negative variance = below budget
Zero variance     = exactly on budget
```

# Budget Variance Percentage Rule

```text
Budget Variance %
=
Budget Variance
/
Budget Transportation Cost
```

If Budget Transportation Cost is zero or missing, the result should be blank.

# Year-over-Year Rules

Year-over-Year comparisons must compare equivalent periods.

Example:

```text
Current Period:
2026-01-01 through 2026-09-30

Comparison Period:
2025-01-01 through 2025-09-30
```

The comparison should not accidentally compare a partial current year against a complete prior year.

# Missing Previous-Year Data

If no valid previous-year value exists, Year-over-Year percentage change should return blank rather than:

- zero
- infinity
- an artificial percentage

# Customer Rules

Each shipment should reference one valid customer.

Customers may be marked as inactive.

Inactive customers remain in historical reporting because historical shipment activity must remain reproducible.

Inactive status should prevent future synthetic activity but should not remove historical records.

# Carrier Rules

A shipment will initially be assigned to one primary carrier.

This simplifies the first version of the model.

Multi-carrier shipments are out of scope for the initial implementation.

If a carrier reference is missing for a shipment that requires transportation, the record should be flagged as a data-quality exception.

# Location Rules

Each shipment should contain:

- one origin location
- one destination location

Origin and destination may reference the same shared Location dimension using role-playing relationships.

A shipment where:

```text
Origin Location = Destination Location
```

is permitted only if a specific business scenario justifies it.

Otherwise it should be treated as suspicious data.

# Region Rule

Every operational location should belong to one region.

Initial regions:

```text
North America
Europe
Latin America
```

Region should normally be derived consistently from Location rather than independently entered on every transaction.

# Route Rule

A route represents an origin-to-destination relationship.

Conceptually:

```text
Route
=
Origin Location + Destination Location
```

Routes may later include additional attributes such as:

- distance
- transportation mode
- expected transit time
- route category

The route identifier should remain stable across repeated shipments between the same origin and destination.

# Asset Rules

Each reusable asset must have a unique Asset ID.

Possible asset statuses may include:

```text
AVAILABLE
IN_USE
IN_TRANSIT
MAINTENANCE
LOST
RETIRED
```

The exact rules governing asset status transitions will be defined during detailed asset modeling.

# Asset Utilization Rule

The initial conceptual definition is:

```text
Asset Utilization %
=
Active Assets
/
Available Assets
```

However, this metric is not considered implementation-ready yet.

Before implementation, the project must define:

- what qualifies as active
- what qualifies as available
- whether utilization is point-in-time or period-based
- how maintenance assets are treated
- how lost or retired assets are treated

A periodic snapshot model may be required.

# Operational Exception Rules

Operational exceptions may include:

```text
LATE_DELIVERY
CANCELLED_SHIPMENT
MISSING_ASSET
DAMAGED_ASSET
COST_ANOMALY
ROUTE_EXCEPTION
```

Each exception should include:

- Exception ID
- Exception Type
- Exception Date
- Severity
- Related business entity where applicable

Possible related entities include:

- Shipment
- Asset
- Customer
- Carrier
- Route
- Location

# Exception Severity

Initial severity levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Severity rules will be defined explicitly during synthetic data generation.

# Duplicate Record Rules

Duplicate records must be evaluated according to business grain.

For example:

```text
Two rows with the same Shipment ID
```

may indicate an invalid shipment duplicate.

But:

```text
Two transportation cost rows for the same Shipment ID
```

may be completely valid if they represent different cost transactions.

Duplicate detection must therefore be based on the expected grain of each table.

# Null Handling

Null values should not automatically be replaced with zero.

The distinction between:

```text
0
```

and:

```text
unknown / missing
```

must be preserved where analytically meaningful.

For example:

```text
Transportation Cost = 0
```

means a known zero cost.

```text
Transportation Cost = NULL
```

means the cost is unknown or unavailable.

These should not be treated as equivalent.

# Data Quality Flags

The project should preserve or generate data-quality indicators for issues such as:

- missing required identifiers
- invalid dates
- duplicate business keys
- missing carrier references
- invalid shipment quantities
- unexpected negative costs
- missing dimensional relationships
- invalid status transitions

These records should remain available for validation and exception analysis rather than being silently discarded.

# Initial Scope Boundaries

The first implementation will assume:

- one primary carrier per shipment
- one customer per shipment
- one origin and one destination per shipment
- calendar-year reporting
- monthly regional budgets
- delivered shipments as the only completed status
- no split deliveries
- no multi-leg shipment modeling
- no currency conversion
- no predictive analytics

These assumptions may be revised later, but changes must be documented before implementation.