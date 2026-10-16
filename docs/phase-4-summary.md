# Phase 4 — PostgreSQL Foundation

## Objective

Establish a reproducible PostgreSQL environment for OpsIntel BI and implement the first database ingestion, validation, staging, performance, and recovery workflows.

## Infrastructure

PostgreSQL runs in Docker using:

```text
PostgreSQL 17
Container: opsintel-postgres
Host port: 5433
Database: opsintel
User: opsintel
```

The host port uses `5433` to avoid conflicts with other local PostgreSQL projects.

## Database Schemas

The database contains three logical schemas:

```text
raw
staging
analytics
```

### raw

Preserves source-like data as received.

The raw layer intentionally allows:

- duplicate business keys
- missing references
- invalid quantities
- impossible dates
- extreme values

### staging

Applies deterministic cleanup and classification logic.

Current staging tables:

```text
staging.shipments_clean
staging.transportation_costs_clean
```

### analytics

Reserved for the dimensional analytical model that will be built in a later phase.

## Raw Ingestion

Current raw tables:

```text
raw.shipments
raw.transportation_costs
```

Input files:

```text
data/raw/shipments.csv
data/raw/transportation_costs.csv
```

The raw layer preserves controlled defects generated during Phase 3.

## Staging Cleanup

Shipment staging logic currently:

- removes duplicate Shipment IDs deterministically
- converts invalid shipment quantities to NULL
- converts impossible delivery dates to NULL
- preserves missing carrier references
- flags problematic records with `quality_status`
- records reasons in `quality_notes`

Transportation-cost staging logic currently:

- preserves valid charge, credit, and reversal transactions
- flags missing shipment references
- flags invalid credit/reversal sign behavior
- preserves extreme values for later analysis rather than deleting them

## Data Quality Validation

Version-controlled SQL validation now exists for:

```text
raw shipment quality
raw transportation-cost quality
raw quality summary
staging shipment quality
staging transportation-cost quality
```

These checks validate conditions such as:

- duplicate shipments
- missing carriers
- invalid quantities
- impossible dates
- duplicate transportation cost IDs
- credit/reversal sign behavior
- quality warning distributions

## Reconciliation Testing

Python integration tests compare PostgreSQL staging output with the clean synthetic reference datasets.

Current reconciliation validates:

- staged shipment row count
- shipment ID coverage
- staged transportation-cost row count
- removal of duplicate shipments
- normalization of invalid quantities
- normalization of impossible delivery dates
- preservation and classification of missing carrier references

## Constraints and Indexes

The staging layer now includes:

- primary keys
- status CHECK constraints
- quality-status CHECK constraints
- transaction-type CHECK constraints
- date indexes
- customer indexes
- carrier indexes
- route indexes
- status indexes
- location indexes
- shipment-to-cost indexes
- compound date/status and shipment/date indexes

Indexes were selected based on expected BI query patterns rather than indexing every column.

## Query Analysis

Representative analytical SQL has been created for:

- shipment volume by month
- carrier delivery performance
- transportation cost by month
- shipment-level transportation cost

`EXPLAIN ANALYZE` examples are included to study:

- sequential scans
- index scans
- bitmap scans
- joins
- aggregates
- planning time
- execution time
- buffer usage

## Database Initialization

The database can now be rebuilt using:

```bash
./scripts/init_database.sh
```

The script:

1. starts PostgreSQL
2. waits for database health
3. creates schemas
4. creates raw tables
5. creates staging tables
6. applies constraints and indexes
7. reloads raw CSV files
8. rebuilds staging tables
9. runs raw data-quality validation

## Backup and Restore

The database can be backed up using:

```bash
./scripts/backup_database.sh
```

Backups are written under:

```text
database/backups/
```

Backup dump files are excluded from Git.

Restore behavior is verified using:

```bash
./scripts/verify_restore.sh
```

The restore script creates a separate test database and validates restored row counts without modifying the working database.

## Phase 4 Architecture

```text
data/raw/
     ↓
PostgreSQL raw schema
     ↓
SQL validation
     ↓
staging cleanup
     ↓
staging schema
     ↓
constraints + indexes
     ↓
query analysis
     ↓
future analytics model
```

## Phase 4 Outcome

OpsIntel BI now has a reproducible PostgreSQL foundation with:

- raw ingestion
- controlled defect preservation
- deterministic staging cleanup
- SQL validation
- integration testing
- indexing
- query-plan analysis
- automated initialization
- backup and restore verification

The project is ready to proceed to the next modeling phase.