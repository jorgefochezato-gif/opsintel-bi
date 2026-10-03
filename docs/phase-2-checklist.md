# Phase 2 — Business Requirements Checklist

## Stakeholder Requirements

- [x] Define executive leadership use cases.
- [x] Define regional operations use cases.
- [x] Define transportation and logistics use cases.
- [x] Define customer operations use cases.
- [x] Define asset operations use cases.
- [x] Define BI / analytics use cases.

## Reporting Requirements

- [x] Define Executive Overview requirements.
- [x] Define Regional Operations requirements.
- [x] Define Carrier Performance requirements.
- [x] Define Customer and Route Analysis requirements.
- [x] Define Operational Exceptions requirements.
- [x] Define filtering requirements.
- [x] Define navigation requirements.
- [x] Define interaction requirements.
- [x] Define security expectations.
- [x] Define initial performance expectations.

## Business Rules

- [x] Define shipment status rules.
- [x] Define on-time delivery logic.
- [x] Define late-shipment logic.
- [x] Define transit-time logic.
- [x] Define shipment count rules.
- [x] Define shipment volume rules.
- [x] Define transportation cost rules.
- [x] Define budget rules.
- [x] Define Year-over-Year comparison rules.
- [x] Define carrier assumptions.
- [x] Define route assumptions.
- [x] Define asset assumptions.
- [x] Define null-handling expectations.
- [x] Define duplicate-handling expectations.
- [x] Define data-quality flags.
- [x] Define scope boundaries.

## Data Requirements

- [x] Define Customer entity requirements.
- [x] Define Carrier entity requirements.
- [x] Define Region entity requirements.
- [x] Define Location entity requirements.
- [x] Define Route entity requirements.
- [x] Define Asset entity requirements.
- [x] Define Shipment entity requirements.
- [x] Define Transportation Cost entity requirements.
- [x] Define Asset Movement entity requirements.
- [x] Define Transportation Budget requirements.
- [x] Define Operational Exception requirements.
- [x] Define Date dimension requirements.
- [x] Define target dataset scale.
- [x] Define historical time range.
- [x] Define reproducibility requirements.
- [x] Define controlled data-quality scenarios.

## Validation

- [x] Define Phase 2 acceptance criteria.
- [ ] Review all Phase 2 documentation.
- [ ] Open Phase 2 pull request.
- [ ] Review PR changes.
- [ ] Merge Phase 2 into `main`.
- [ ] Synchronize local `main`.

## Phase 2 Deliverables

```text
docs/
├── phase-2-checklist.md
└── requirements/
    ├── stakeholder-use-cases.md
    ├── report-requirements.md
    ├── business-rules.md
    ├── data-requirements.md
    └── phase-2-acceptance-criteria.md
```

## Next Phase

**Phase 3 — Synthetic Operational Dataset**

Phase 3 will convert these requirements into deterministic Python-based data generation.

Planned work includes:

- Python project setup
- random-seed strategy
- master-data generation
- transaction generation
- controlled data-quality defects
- dataset validation
- generated CSV outputs
- reproducibility tests