# Phase 2 — Acceptance Criteria

## Purpose

This document defines the criteria that must be satisfied before OpsIntel BI can move from requirements definition into synthetic data generation.

## Business Requirements

Phase 2 is acceptable when:

- stakeholder groups are clearly identified
- each stakeholder group has documented analytical use cases
- major business questions are documented
- KPI definitions are documented
- report expectations are documented
- business rules and edge cases are documented
- initial data requirements are documented
- initial scope boundaries are explicit

## KPI Requirements

Each major KPI should include, where applicable:

- business meaning
- conceptual formula
- numerator
- denominator
- date context
- exclusions
- division-by-zero behavior
- validation approach

KPIs that are not yet implementation-ready must be clearly marked as requiring further modeling decisions.

## Report Requirements

The reporting specification should define:

- intended audience
- primary business objective
- required KPIs
- expected analysis
- filtering behavior
- navigation expectations
- security expectations
- acceptance criteria

## Business Rule Requirements

Business rules must explicitly address:

- shipment status handling
- cancelled shipments
- late-delivery logic
- missing delivery dates
- invalid date sequences
- duplicate records
- transportation-cost multiplicity
- negative costs
- budget grain
- zero-budget handling
- previous-year comparisons
- inactive customers and carriers
- route integrity
- null handling
- controlled data-quality exceptions

## Data Requirements

The data specification should define:

- required entities
- business keys
- required attributes
- expected relationships
- initial valid status values
- expected fact-table grain
- historical date range
- target dataset size
- controlled data-quality scenarios
- reproducibility requirements

## Analytical Readiness

Phase 2 is complete when the documentation is sufficient to answer:

1. What business problem are we solving?
2. Who will use the solution?
3. What questions must the solution answer?
4. Which KPIs are required?
5. What rules govern those KPIs?
6. What data is required?
7. What relationships must exist?
8. What known edge cases must be handled?
9. What is explicitly out of scope?
10. What must be validated later in SQL and Power BI?

## Exit Condition

Phase 2 may transition into Phase 3 only when the requirements are detailed enough to design a deterministic synthetic data generator without inventing major business rules during implementation.