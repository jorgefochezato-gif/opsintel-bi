# Phase 4 — PostgreSQL Foundation Checklist

## Infrastructure

- [x] Add Docker Compose PostgreSQL service.
- [x] Use PostgreSQL 17.
- [x] Configure isolated local host port.
- [x] Add container health check.
- [x] Verify PostgreSQL connectivity.

## Schemas

- [x] Create `raw` schema.
- [x] Create `staging` schema.
- [x] Create `analytics` schema.

## Raw Layer

- [x] Create raw shipment table.
- [x] Create raw transportation-cost table.
- [x] Load raw shipment CSV.
- [x] Load raw transportation-cost CSV.
- [x] Preserve known source defects.
- [x] Validate raw row counts.
- [x] Validate duplicate shipments.
- [x] Validate missing carriers.
- [x] Validate invalid quantities.
- [x] Validate invalid delivery dates.
- [x] Validate transportation-cost anomalies.

## Staging Layer

- [x] Create staged shipment table.
- [x] Create staged transportation-cost table.
- [x] Deduplicate shipments.
- [x] Normalize invalid quantities.
- [x] Normalize impossible delivery dates.
- [x] Preserve missing references.
- [x] Add quality-status classification.
- [x] Add quality notes.
- [x] Validate staging output.

## Reconciliation

- [x] Compare staging shipment count to clean reference.
- [x] Compare shipment ID coverage to clean reference.
- [x] Verify duplicate removal.
- [x] Verify invalid quantity cleanup.
- [x] Verify invalid delivery-date cleanup.
- [x] Verify missing carriers remain traceable.
- [x] Add automated database reconciliation tests.

## Constraints and Indexes

- [x] Add staging primary keys.
- [x] Add CHECK constraints.
- [x] Add date indexes.
- [x] Add carrier indexes.
- [x] Add customer indexes.
- [x] Add route indexes.
- [x] Add status indexes.
- [x] Add location indexes.
- [x] Add shipment-to-cost indexes.
- [x] Add compound indexes for representative query patterns.

## Query Analysis

- [x] Create representative analytical SQL queries.
- [x] Add `EXPLAIN ANALYZE` examples.
- [x] Inspect index usage.
- [x] Review PostgreSQL query planner behavior.

## Automation

- [x] Create repeatable database initialization script.
- [x] Rebuild raw ingestion automatically.
- [x] Rebuild staging automatically.
- [x] Add automated raw validation during initialization.

## Backup and Restore

- [x] Create backup directory.
- [x] Exclude dump files from Git.
- [x] Create database backup script.
- [x] Create restore verification script.
- [x] Restore into isolated test database.
- [x] Verify restored row counts.

## Phase Closure

- [ ] Run complete automated test suite.
- [ ] Run initialization from current repository state.
- [ ] Run backup.
- [ ] Run restore verification.
- [ ] Review Phase 4 Git diff.
- [ ] Push feature branch.
- [ ] Open Phase 4 pull request.
- [ ] Review Phase 4 pull request.
- [ ] Merge into `main`.
- [ ] Synchronize local `main`.
- [ ] Delete completed feature branch.
- [ ] Sync GitHub Project status.

## Next Phase

The next phase will build the analytical dimensional model on top of the validated staging layer.