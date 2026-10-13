# Phase 4 — PostgreSQL Foundation Checklist

Status: **In Progress locally**. Last checked: 2026-10-13.
Tracking: [issue #6](https://github.com/jorgefochezato-gif/opsintel-bi/issues/6).
Source: [development conversation](https://chatgpt.com/share/6ace94d4-5aa4-83e9-941e-0a01126b84a9).

Implementation instructions exist for the first sections below. Checkboxes remain unchecked until the saved implementation and execution evidence are supplied or verified. This avoids treating proposed commands as successful execution.

## Infrastructure and ingestion

- [ ] Confirm local feat/phase-4-postgresql-foundation branch and commit.
- [ ] Configure Docker PostgreSQL service, persistent volume, health check, and port mapping.
- [ ] Verify startup and database connectivity.
- [ ] Create raw, staging, and analytics schemas.
- [ ] Define raw shipments and transportation_costs tables.
- [ ] Load source-like CSVs repeatably while retaining controlled defects.
- [ ] Record raw counts and source reconciliation.
- [ ] Document explicit source mappings for any additional master/reference tables.

## Cleanup and validation

- [ ] Save and run raw shipment/cost quality queries and summary.
- [ ] Create staging shipments_clean and transportation_costs_clean tables.
- [ ] Load staging with documented duplicate selection and warning rules.
- [ ] Verify warning-compatible handling of invalid dates, quantities, missing references, and extreme costs.
- [ ] Save and run staging SQL quality queries.
- [ ] Add psycopg dependency and refresh the dependency lock.
- [ ] Save and run Python staging reconciliation tests.
- [ ] Capture full-suite results and required database/data prerequisites.
- [ ] Record counts, IDs, quality findings, and reconciliation limits.
- [ ] Compare detected defects with the injected defect manifest using explicitly defined matching rules.

## Remaining engineering work

- [ ] Review duplicate timestamp ties and deterministic selection.
- [ ] Review primary keys, appropriate constraints, and indexes.
- [ ] Review reference existence checks and compound quality-note checks.
- [ ] Capture applicable query plans and performance observations.
- [ ] Verify backup and restore in a separate test database.
- [ ] Reconcile post-restore counts and integrity checks.

## Documentation and closure

- [x] Document local progress and evidence boundary.
- [x] Document setup sequence, quality decisions, and validation limits.
- [ ] Replace expected outcomes with captured execution evidence.
- [ ] Push implementation branch and link partial PRs with Refs #6.
- [ ] Review and merge final implementation PR with Closes #6.
- [ ] Synchronize local main and phase documentation.
- [ ] Close issue #6 as completed and set project Done only after verified merge.

The documentation tasks describe this documentation update only. Phase 4 implementation remains in progress.

