# KPI Catalog

This document defines the initial business metrics for OpsIntel BI.

Each KPI should have a clear business meaning, reproducible calculation, expected grain, and validation method before implementation in SQL or DAX.

## 1. Total Transportation Cost

### Business Meaning

Total transportation spend incurred for shipments within the selected reporting context.

### Conceptual Formula

```text
Total Transportation Cost
=
SUM(Transportation Cost Amount)
```

### Primary Dimensions

- Date
- Region
- Location
- Customer
- Carrier
- Route

### Validation

The Power BI measure must match an equivalent SQL `SUM()` calculation over the same filtered records.

---

## 2. Shipment Count

### Business Meaning

Number of distinct shipments within the selected reporting context.

### Conceptual Formula

```text
Shipment Count
=
COUNT DISTINCT Shipment ID
```

### Validation

Power BI must match a SQL `COUNT(DISTINCT shipment_id)` calculation.

---

## 3. Cost per Shipment

### Business Meaning

Average transportation cost required to complete one shipment.

### Conceptual Formula

```text
Cost per Shipment
=
Total Transportation Cost
/
Shipment Count
```

### Validation

Compare Power BI results against the equivalent SQL aggregation.

---

## 4. On-Time Delivery Percentage

### Business Meaning

Percentage of completed shipments delivered on or before their expected delivery date.

### Conceptual Formula

```text
On-Time Delivery %
=
On-Time Shipments
/
Completed Shipments
```

### Important Definition

A shipment is considered on time when:

```text
Actual Delivery Date <= Expected Delivery Date
```

Cancelled shipments should not be included in the denominator.

### Validation

Validate both numerator and denominator independently using SQL.

---

## 5. Late Shipment Rate

### Business Meaning

Percentage of completed shipments delivered after the expected delivery date.

### Conceptual Formula

```text
Late Shipment Rate
=
Late Shipments
/
Completed Shipments
```

### Important Definition

A shipment is late when:

```text
Actual Delivery Date > Expected Delivery Date
```

---

## 6. Average Transit Time

### Business Meaning

Average elapsed time between shipment departure and delivery.

### Conceptual Formula

```text
Transit Time
=
Actual Delivery Date
-
Shipment Date
```

```text
Average Transit Time
=
AVERAGE(Transit Time)
```

### Unit

Days.

---

## 7. Asset Utilization Percentage

### Business Meaning

Percentage of available reusable assets actively being used during the selected reporting period.

### Initial Conceptual Formula

```text
Asset Utilization %
=
Active Assets
/
Available Assets
```

### Design Note

The precise definition of "active" and "available" will be finalized during asset-movement modeling because utilization may depend on time and asset status.

---

## 8. Shipment Volume

### Business Meaning

Total quantity of reusable assets or units transported.

### Conceptual Formula

```text
Shipment Volume
=
SUM(Shipment Quantity)
```

### Design Note

Shipment Count and Shipment Volume are deliberately separate metrics.

One shipment may contain multiple assets or units.

---

## 9. Year-to-Date Transportation Cost

### Business Meaning

Transportation spend accumulated from the beginning of the current calendar year through the selected date.

### Conceptual Formula

```text
YTD Transportation Cost
=
Transportation Cost from January 1
through selected date
```

### Validation

Validate against SQL using date filtering based on the reporting date.

---

## 10. Previous-Year Transportation Cost

### Business Meaning

Transportation cost for the equivalent reporting period one year earlier.

### Example

If the current reporting context is:

```text
January 1, 2026 through September 30, 2026
```

the comparable previous-year period should be:

```text
January 1, 2025 through September 30, 2025
```

---

## 11. Year-over-Year Cost Change

### Business Meaning

Absolute change in transportation cost compared with the equivalent period in the previous year.

### Conceptual Formula

```text
YoY Cost Change
=
Current Transportation Cost
-
Previous-Year Transportation Cost
```

---

## 12. Year-over-Year Cost Change Percentage

### Business Meaning

Percentage change in transportation cost compared with the equivalent period in the previous year.

### Conceptual Formula

```text
YoY Cost Change %
=
(Current Cost - Previous-Year Cost)
/
Previous-Year Cost
```

### Edge Case

If previous-year transportation cost is zero, the result should return blank rather than divide by zero.

---

## 13. Budget Variance

### Business Meaning

Absolute difference between actual transportation cost and budgeted transportation cost.

### Conceptual Formula

```text
Budget Variance
=
Actual Transportation Cost
-
Budget Transportation Cost
```

### Interpretation

A positive result indicates spending above budget.

A negative result indicates spending below budget.

---

## 14. Budget Variance Percentage

### Business Meaning

Transportation cost variance expressed relative to the budget.

### Conceptual Formula

```text
Budget Variance %
=
Budget Variance
/
Budget Transportation Cost
```

### Edge Case

If budget transportation cost is zero, the metric should return blank.

---

## 15. Carrier Cost per Shipment

### Business Meaning

Average transportation cost per shipment for a carrier.

### Conceptual Formula

```text
Carrier Cost per Shipment
=
Carrier Transportation Cost
/
Carrier Shipment Count
```

### Primary Use

Supports comparison of carrier economics across regions and routes.

---

## 16. Carrier On-Time Delivery Percentage

### Business Meaning

Percentage of completed shipments delivered on time by each carrier.

### Conceptual Formula

```text
Carrier On-Time Delivery %
=
Carrier On-Time Shipments
/
Carrier Completed Shipments
```

### Primary Use

Supports comparison of carrier service quality.

---

# Metric Design Principles

All metrics in OpsIntel BI should follow these principles:

1. A KPI must have a documented business definition.
2. Numerator and denominator must be explicitly defined where applicable.
3. The relevant date field must be known.
4. Exclusions must be documented.
5. Filter behavior must be predictable.
6. SQL and Power BI results must be reconcilable.
7. Division-by-zero behavior must be defined.
8. Time-intelligence metrics must use a governed Date dimension.
9. KPI definitions should remain independent of report visualization.
10. Any change to a KPI definition should be documented before implementation.

# Open Questions

The following items will be resolved during later design phases:

- Exact definition of an available asset.
- Exact definition of an active asset.
- Whether utilization should be point-in-time or period-based.
- How cancelled shipments affect operational metrics.
- Whether partial deliveries exist.
- Whether transportation costs can span multiple cost records per shipment.
- How route definitions should be modeled.
- Budget granularity.
- Fiscal year versus calendar year requirements.