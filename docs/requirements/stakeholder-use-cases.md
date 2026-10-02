# Stakeholder Use Cases

## Purpose

This document defines how different stakeholder groups are expected to use OpsIntel BI.

The goal is to translate broad business needs into concrete analytical use cases that can later be mapped to data requirements, KPIs, report pages, and acceptance criteria.

## Executive Leadership

### Use Case 1 — Monitor Enterprise Transportation Cost

**As an executive leader,**

I want to monitor transportation cost across the organization

**so that**

I can identify material changes in spending and determine where management attention is required.

### Key Questions

- What is total transportation cost?
- How has cost changed compared with the previous year?
- Which regions are driving the largest increases?
- Is actual spending above or below budget?
- Are higher costs associated with higher shipment volume?

### Expected Metrics

- Total Transportation Cost
- YTD Transportation Cost
- Previous-Year Transportation Cost
- YoY Cost Change
- YoY Cost Change Percentage
- Budget Variance
- Budget Variance Percentage
- Shipment Volume

### Expected Analysis

The user should be able to compare:

```text
Current Period
vs
Previous Year
vs
Budget
```

and drill into region-level drivers.

---

### Use Case 2 — Monitor Service Performance

**As an executive leader,**

I want to understand delivery performance across the network

**so that**

I can determine whether cost changes are associated with changes in customer service.

### Key Questions

- What percentage of shipments are delivered on time?
- Is on-time performance improving or deteriorating?
- Which regions or carriers are underperforming?
- Are late shipments increasing transportation cost?

### Expected Metrics

- On-Time Delivery Percentage
- Late Shipment Rate
- Average Transit Time
- Shipment Count

---

## Regional Operations Manager

### Use Case 3 — Investigate Regional Performance

**As a regional operations manager,**

I want to analyze operational and financial performance within my region

**so that**

I can identify areas requiring corrective action.

### Key Questions

- Which locations are generating the highest transportation cost?
- Which carriers have the highest late-shipment rate?
- Which customers generate the most operational exceptions?
- Which routes show declining performance?
- Is asset utilization lower than expected?

### Expected Metrics

- Total Transportation Cost
- Cost per Shipment
- Shipment Count
- Shipment Volume
- Late Shipment Rate
- On-Time Delivery Percentage
- Asset Utilization Percentage
- Exception Count

### Security Requirement

The manager should only be able to access data assigned to the manager's region.

---

## Transportation and Logistics Team

### Use Case 4 — Compare Carrier Performance

**As a transportation analyst,**

I want to compare carriers across cost and service metrics

**so that**

I can identify opportunities for carrier optimization.

### Key Questions

- Which carriers have the lowest cost per shipment?
- Which carriers have the strongest on-time performance?
- Which carriers show increasing costs?
- Are low-cost carriers associated with poor service?
- Which carriers generate the most exceptions?

### Expected Metrics

- Carrier Cost per Shipment
- Carrier On-Time Delivery Percentage
- Shipment Count
- Total Transportation Cost
- Average Transit Time
- Exception Count

---

### Use Case 5 — Analyze Route Performance

**As a transportation analyst,**

I want to evaluate transportation routes

**so that**

I can identify inefficient or unreliable lanes.

### Key Questions

- Which routes have the highest cost per shipment?
- Which routes have the highest late-shipment rates?
- Which routes have the longest transit times?
- Which routes show abnormal cost increases?
- Which regions contain the weakest-performing routes?

### Expected Dimensions

- Origin Location
- Destination Location
- Route
- Region
- Carrier
- Date

---

## Customer Operations Team

### Use Case 6 — Analyze Customer Service Performance

**As a customer operations analyst,**

I want to evaluate service performance by customer

**so that**

I can identify accounts experiencing operational problems.

### Key Questions

- Which customers receive the highest shipment volume?
- Which customers experience the most late deliveries?
- Which customers generate the most transportation cost?
- Which customers show deteriorating service trends?
- Which customers generate the most exceptions?

### Expected Metrics

- Shipment Count
- Shipment Volume
- Total Transportation Cost
- Cost per Shipment
- On-Time Delivery Percentage
- Late Shipment Rate
- Exception Count

---

## Asset Operations Team

### Use Case 7 — Monitor Reusable Asset Utilization

**As an asset operations analyst,**

I want to understand how reusable assets move through the network

**so that**

I can identify low utilization, imbalances, or operational bottlenecks.

### Key Questions

- How many assets are available?
- How many assets are active?
- What is the utilization rate?
- Which regions show low utilization?
- Where are assets accumulating?
- Which locations experience unusual movement patterns?

### Expected Metrics

- Active Asset Count
- Available Asset Count
- Asset Utilization Percentage
- Asset Movement Count

### Modeling Note

The final utilization calculation may require a periodic snapshot fact table rather than relying only on asset movement events.

---

## BI / Analytics Team

### Use Case 8 — Validate Reported Metrics

**As a BI analyst,**

I want to reproduce important Power BI metrics independently using SQL

**so that**

I can confirm that published reports are accurate and trustworthy.

### Key Requirements

- Major KPIs must have SQL validation queries.
- Numerators and denominators must be testable independently.
- Date filters must be explicitly defined.
- Edge cases must be documented.
- SQL and DAX outputs must reconcile within the same reporting context.

---

### Use Case 9 — Maintain a Governed Semantic Model

**As a BI developer,**

I want to maintain a reusable Power BI semantic model

**so that**

multiple reports can rely on consistent business logic.

### Key Requirements

- Reusable measures
- Consistent dimension usage
- Controlled relationships
- Hidden technical fields
- Clear business naming
- Row-Level Security
- Documented calculation logic
- Predictable filter behavior

---

# Cross-Functional Requirements

The analytical solution should support:

- filtering by date
- filtering by region
- filtering by customer
- filtering by carrier
- filtering by route
- drill-down from enterprise to regional detail
- comparison with previous periods
- comparison with budget
- exception identification
- SQL-to-Power-BI validation
- secure regional access

# Design Principle

Each report page and visual should exist to support one or more documented stakeholder use cases.

A visualization should not be added only because the data is available.