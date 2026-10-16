# Local PostgreSQL Setup and Validation

Status: Phase 4 is completed and published in merged [PR #22](https://github.com/jorgefochezato-gif/opsintel-bi/pull/22), checked 2026-10-16. The commands below match the published files. PR #22 reports successful database checks; this synchronization did not rerun Docker/WSL execution.

## Prerequisites and configuration

- Docker with Compose support; run from the repository root.
- The project's Python environment and locked dependencies.
- Generated clean/reference and raw CSVs from the Phase 3 generator.
- Published Docker Compose, schema, ingestion, staging, and validation files.

The published service uses PostgreSQL 17, database/user opsintel, container opsintel-postgres, and named volume opsintel_postgres_data. The host connection is localhost:5433; PostgreSQL inside the container listens on 5432. Use the local Compose credentials; example development credentials must not be treated as production configuration.

## Start and inspect

```bash
docker compose up -d
docker compose ps
docker compose logs postgres
docker compose exec postgres pg_isready -U opsintel -d opsintel
```

Expected: service healthy and accepting connections. Record the actual output rather than assuming it succeeded. For local reloads, reuse the volume and apply the scripts in order; do not delete the database volume as a reload procedure.

## Schema and load order

Run the Phase 3 generator before initialization:

```bash
python -m pip install -r requirements-lock.txt
python scripts/data_generation/generate.py
bash scripts/init_database.sh
```

`init_database.sh` starts the service, waits for readiness, creates schemas and tables, applies constraints/indexes, truncates and loads both raw CSVs, rebuilds both staging tables, and prints the raw quality summary. It uses `psql` without `ON_ERROR_STOP`; inspect output for SQL errors rather than treating its final message as a strict success gate.

The following commands use Bash/WSL input redirection, matching the development conversation; they are not PowerShell syntax.

```bash
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < database/schema/002_create_raw_tables.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/validation/raw_shipments_quality.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/validation/raw_transportation_costs_quality.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/validation/raw_quality_summary.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < database/schema/003_create_staging_tables.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/staging/load_shipments_clean.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/staging/load_transportation_costs_clean.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/validation/staging_shipments_quality.sql
docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -U opsintel -d opsintel < sql/validation/staging_transportation_costs_quality.sql
```

The staging scripts truncate their destination tables. They are full reloads: ensure the intended local database is selected, then run the steps in order. Initialization explicitly truncates raw tables before loading CSVs.

## Python dependencies and tests

The published requirements and lock include psycopg and its binary package. Install the checked-in lock for repeatability; when intentionally changing dependencies, update and review the lock.

```bash
python -m pip install -r requirements-lock.txt
pytest -q tests/test_staging_reconciliation.py
pytest -q
```

Database tests require the running database, loaded staging tables, and matching generated/raw CSVs. The database test uses localhost:5433. Running inside a container would require a different host/service address. Generator reproducibility tests regenerate CSVs; ensure the database load matches that generator configuration before interpreting reconciliation failures.

## Evidence to capture

Record the implementation SHA, database/Python versions, dependency lock, schema list, load commands, raw/staging row counts, warning counts, SQL outputs, pytest summary, and failures or unresolved assumptions. On 2026-10-16, the generator completed and `python -m pytest -q tests/test_generated_data.py` passed: 12 passed in 6.81s, using Python 3.12 and the pinned packages at implementation head fec7936 / merge b30e726. Reproducibility and database tests were not independently rerun. Database rebuild, backup, and restore remain PR #22-reported results without captured logs.

## Backup and restore

Published commands (Bash/WSL):

```bash
bash scripts/backup_database.sh
bash scripts/verify_restore.sh
```

Backup writes `database/backups/opsintel.dump` (excluded from Git). Restore recreates the isolated `opsintel_restore_test` database and prints raw/staging row counts. It leaves the working database intact, but recreates any existing restore-test database. The script does not assert count equality, compare keys or quality distributions, or prove full restored integrity; perform and record those comparisons separately.

See [Phase 4 checklist](phase-4-checklist.md) and [quality decisions](decisions/raw-staging-data-quality.md).

