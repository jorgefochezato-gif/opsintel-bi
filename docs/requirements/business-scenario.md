# Business Scenario

## Overview

OpsIntel BI simulates an enterprise operations and supply-chain analytics environment for a company that manages a large network of reusable logistics assets, shipments, carriers, customers, and regional operations.

The organization operates across multiple regions and needs better visibility into transportation cost, shipment performance, asset utilization, carrier performance, and operational exceptions.

The purpose of the project is to design and implement an end-to-end business intelligence solution that turns operational data into validated, decision-ready reporting for leadership and operational teams.

## Business Context

The company manages a large volume of shipments and reusable assets across multiple regions.

Operational data exists across several business processes, including:

- customer shipments
- transportation activity
- carrier performance
- asset movement
- transportation cost
- regional operations
- delivery performance

Leadership currently lacks a unified analytical view across these areas.

Different teams may calculate similar metrics differently, making it difficult to establish a trusted source of truth.

The organization needs a governed analytics solution that provides consistent KPIs, clear definitions, secure access, and the ability to investigate performance drivers.

## Primary Business Problem

Transportation costs are increasing, but leadership does not have enough visibility into the operational drivers behind those increases.

Management needs to understand whether higher costs are being driven by factors such as:

- shipment volume
- specific regions
- customers
- carriers
- routes
- delivery delays
- asset utilization
- transportation distance
- seasonal changes
- operational exceptions

The organization also needs to determine whether increasing costs are associated with improvements or deterioration in service performance.

## Stakeholders

### Executive Leadership

Needs a high-level view of overall operational and financial performance.

Primary concerns:

- total transportation cost
- cost trends
- budget performance
- service levels
- asset utilization
- regional performance

### Regional Operations Managers

Need visibility into operational performance within their assigned regions.

Primary concerns:

- shipment volume
- late shipments
- transportation cost
- carrier performance
- asset movement
- utilization
- operational exceptions

### Transportation and Logistics Team

Needs detailed analysis of transportation efficiency.

Primary concerns:

- carrier cost
- cost per shipment
- delivery performance
- transit time
- route performance
- cost variance
- carrier reliability

### Customer Operations Team

Needs visibility into customer-level activity and service performance.

Primary concerns:

- shipment volume by customer
- delivery performance
- transportation cost
- exception rates
- customer trends

### BI / Analytics Team

Responsible for providing a reliable and governed analytical solution.

Primary concerns:

- metric consistency
- data quality
- semantic model design
- calculation accuracy
- security
- report performance
- maintainability

## Core Business Questions

The analytical solution should help answer questions including:

1. What is the total transportation cost?
2. How is transportation cost changing over time?
3. How does current performance compare with the previous year?
4. Which regions contribute most to transportation cost?
5. Which customers generate the highest transportation cost?
6. Which carriers have the highest cost per shipment?
7. Which carriers have the strongest and weakest delivery performance?
8. What percentage of shipments are delivered on time?
9. Which routes experience the highest late-shipment rates?
10. Are late shipments associated with higher transportation costs?
11. How efficiently are reusable assets being utilized?
12. Which regions have the lowest asset utilization?
13. How does shipment volume affect transportation cost?
14. Which operational factors are driving cost variance?
15. Which areas require management attention?

## Initial KPI Candidates

The first version of the analytical solution is expected to include metrics such as:

- Total Transportation Cost
- Shipment Count
- Cost per Shipment
- Cost per Asset
- On-Time Delivery Percentage
- Late Shipment Rate
- Average Transit Time
- Asset Utilization Percentage
- Shipment Volume
- Year-to-Date Transportation Cost
- Previous-Year Transportation Cost
- Year-over-Year Cost Change
- Year-over-Year Cost Change Percentage
- Budget Variance
- Budget Variance Percentage

The final KPI definitions will be documented separately before implementation.

## Analytical Scope

The solution will initially focus on:

- transportation cost
- shipment performance
- carrier performance
- customer activity
- regional operations
- reusable asset utilization
- operational exceptions

The project will use approximately three years of synthetic historical operational data to support trend and time-intelligence analysis.

## Geographic Scope

The synthetic company will operate across multiple geographic regions.

The exact hierarchy will be defined during data-model design but is expected to include concepts such as:

```text
Global
  ├── North America
  ├── Europe
  └── Latin America
```

Each region will contain multiple operational locations.

## Data Characteristics

The project will simulate enterprise-scale operational data containing:

- customers
- carriers
- locations
- regions
- reusable assets
- shipments
- asset movements
- transportation costs
- dates
- operational exceptions

The synthetic dataset will intentionally include realistic data-quality conditions such as:

- missing values
- duplicate records
- outliers
- delayed shipments
- inactive customers
- inconsistent operational records

These conditions will be used to demonstrate data-quality and validation practices.

## Solution Objectives

The completed solution should provide:

1. A centralized analytical data model.
2. Consistent KPI definitions.
3. SQL-based transformation and validation logic.
4. A dimensional star-schema model.
5. A governed Power BI semantic model.
6. Reusable DAX measures.
7. Row-Level Security.
8. Interactive executive and operational reports.
9. SQL-to-Power-BI metric validation.
10. Documentation of architecture, calculations, and design decisions.

## Success Criteria

The project will be considered successful when:

- business requirements are documented
- KPI definitions are explicit and reproducible
- data relationships are clearly modeled
- SQL calculations match Power BI measures
- reports answer the documented business questions
- Row-Level Security behaves as designed
- key measures are validated
- documentation explains major design decisions
- the complete solution can be presented as a professional portfolio case study