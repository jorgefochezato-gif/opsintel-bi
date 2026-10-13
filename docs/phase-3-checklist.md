# Phase 3 — Synthetic Operational Dataset Checklist

## Python Foundation

- [x] Create Python virtual environment.
- [x] Define project dependencies.
- [x] Create dependency lock file.
- [x] Establish generator package structure.
- [x] Define deterministic random seed.
- [x] Define reporting period.
- [x] Define configurable dataset sizes.

## Master Data

- [x] Generate Regions.
- [x] Generate geographically coherent Locations.
- [x] Generate Customers.
- [x] Generate Carriers.
- [x] Define carrier service profiles.
- [x] Generate Routes.
- [x] Calculate route distance.
- [x] Generate reusable Assets.

## Transactional Data

- [x] Generate Shipments.
- [x] Model shipment status behavior.
- [x] Model on-time and late deliveries.
- [x] Generate Transportation Costs.
- [x] Generate multiple cost transactions per shipment.
- [x] Generate credits and corrections.
- [x] Generate monthly regional Transportation Budgets.
- [x] Generate Asset Movement history.
- [x] Generate Operational Exceptions.

## Analytical Behavior

- [x] Connect carrier profile to service performance.
- [x] Connect carrier profile to transportation cost.
- [x] Connect distance to transportation cost.
- [x] Connect shipment quantity to transportation cost.
- [x] Create seasonal budget behavior.
- [x] Generate cost-versus-service trade-offs.
- [x] Derive operational exceptions from generated activity.

## Data Quality

- [x] Preserve clean reference datasets.
- [x] Create raw source-like datasets.
- [x] Inject duplicate shipments.
- [x] Inject missing carrier references.
- [x] Inject invalid delivery dates.
- [x] Inject invalid shipment quantities.
- [x] Inject extreme transportation costs.
- [x] Create data-quality issue manifest.
- [x] Separate `data/generated/` and `data/raw/`.

## Automated Validation

- [x] Validate Regions.
- [x] Validate Locations.
- [x] Validate Customers.
- [x] Validate Carriers.
- [x] Validate Routes.
- [x] Validate Assets.
- [x] Validate Shipments.
- [x] Validate Transportation Costs.
- [x] Validate Transportation Budgets.
- [x] Validate Asset Movements.
- [x] Validate Operational Exceptions.
- [x] Validate controlled raw-source defects.
- [x] Add reproducibility test.
- [x] Verify repeated generator runs produce identical datasets.

## Documentation

- [x] Document generated/raw data separation.
- [x] Document Phase 3 implementation.
- [x] Document reproducibility strategy.
- [x] Document Phase 4 ingestion boundary.

## Phase Closure

- [ ] Run complete automated test suite.
- [ ] Review working tree.
- [ ] Review Phase 3 commit history.
- [ ] Push feature branch.
- [ ] Open Phase 3 pull request.
- [ ] Review Phase 3 PR.
- [ ] Merge Phase 3 into `main`.
- [ ] Synchronize local `main`.
- [ ] Delete completed feature branch.
- [ ] Update GitHub Project status.

## Next Phase

**Phase 4 — PostgreSQL Foundation**

Planned work includes:

- Docker PostgreSQL service
- database initialization
- `raw`, `staging`, and `analytics` schemas
- raw-table definitions
- CSV ingestion
- constraints and indexes
- data-quality validation queries
- staging cleanup logic
- backup and restore verification