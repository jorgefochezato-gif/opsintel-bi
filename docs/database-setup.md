# Local PostgreSQL Setup and Validation

Status: Phase 4 local development procedure from the [conversation](https://chatgpt.com/share/6ace94d4-5aa4-83e9-941e-0a01126b84a9). Phase 4 implementation files and execution results have not yet been verified in GitHub main. Run these commands only in the local implementation checkout after confirming the named files exist.

## Prerequisites and configuration

- Docker with Compose support; run from the repository root.
- The project's Python environment and locked dependencies.
- Generated clean/reference and raw CSVs from the Phase 3 generator.
- Local Phase 4 Docker Compose, schema, ingestion, staging, and validation files.

The discussed service uses PostgreSQL 17, database/user opsintel, container opsintel-postgres, and named volume opsintel_postgres_data. The host connection is localhost:5433; PostgreSQL inside the container listens on 5432. This keeps the discussed OpsHub port 5432 separate. Use the local Compose credentials; example development credentials must not be treated as production configuration.

## Start and inspect

```bash
docker compose up -d
docker compose ps
docker compose logs postgres
docker compose exec postgres pg_isready -U opsintel -d opsintel
```

Expected: service healthy and accepting connections. Record the actual output rather than assuming it succeeded. For local reloads, reuse the volume and apply the scripts in order; do not delete the database volume as a reload procedure.

## Schema and load order

1. Create raw, staging, and analytics schemas using the local initialization script.
2. Apply database/schema/002_create_raw_tables.sql.
3. Run the local CSV ingestion script for raw shipments and transportation costs.
4. Run raw quality checks and record baseline counts.
5. Apply database/schema/003_create_staging_tables.sql.
6. Run staging shipment cleanup, then staging cost cleanup.
7. Run staging SQL validation and Python reconciliation.

The initialization and ingestion script names must be confirmed against the implementation before adding exact commands here. Do not ingest clean shipment CSVs in place of the defect-bearing raw sources.

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

The proposed staging scripts truncate their destination tables. They are full reloads: ensure the intended local database is selected, then run the steps in order. Raw CSV reloads also need an explicit reset/append policy in the implementation to avoid accumulating duplicates.

## Python dependencies and tests

The conversation proposes psycopg[binary] in requirements.txt and a refreshed requirements-lock.txt. Verify these changes exist before running database tests. Install the checked-in lock for repeatability; when intentionally changing dependencies, update and review the lock.

```bash
python -m pip install -r requirements-lock.txt
pytest -q tests/test_staging_reconciliation.py
pytest -q
```

Database tests require the running database, loaded staging tables, and matching generated/raw CSVs. The proposed test uses localhost:5433. Running inside a container would require a different host/service address. Generator reproducibility tests regenerate CSVs; ensure the database load matches that generator configuration before interpreting reconciliation failures.

## Evidence to capture

Record the implementation SHA, database/Python versions, dependency lock, schema list, load commands, raw/staging row counts, warning counts, SQL outputs, pytest summary, and failures or unresolved assumptions. No measured Phase 4 results are supplied by this documentation update.

## Backup and restore

Backup/restore verification remains pending. Test restore into a separate database, then compare counts, keys, quality distributions, and relevant schema objects. Record the dump/restore commands and results once the local implementation procedure is verified.

See [Phase 4 checklist](phase-4-checklist.md) and [quality decisions](decisions/raw-staging-data-quality.md).

