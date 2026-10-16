#!/usr/bin/env bash

set -euo pipefail

echo "Starting OpsIntel BI database initialization..."

docker compose up -d

echo "Waiting for PostgreSQL..."

until docker compose exec -T postgres \
  pg_isready -U opsintel -d opsintel > /dev/null 2>&1
do
  sleep 1
done

echo "PostgreSQL is ready."

echo "Creating schemas..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < database/schema/001_create_schemas.sql

echo "Creating raw tables..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < database/schema/002_create_raw_tables.sql

echo "Creating staging tables..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < database/schema/003_create_staging_tables.sql

echo "Applying staging constraints and indexes..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < database/schema/004_add_staging_constraints_indexes.sql

echo "Clearing raw tables..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  -c "TRUNCATE TABLE raw.transportation_costs, raw.shipments;"

echo "Loading raw shipments..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  -c "\copy raw.shipments FROM STDIN WITH (FORMAT csv, HEADER true)" \
  < data/raw/shipments.csv

echo "Loading raw transportation costs..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  -c "\copy raw.transportation_costs FROM STDIN WITH (FORMAT csv, HEADER true)" \
  < data/raw/transportation_costs.csv

echo "Loading cleaned staging shipments..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < sql/staging/load_shipments_clean.sql

echo "Loading cleaned staging transportation costs..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < sql/staging/load_transportation_costs_clean.sql

echo "Running raw validation summary..."
docker compose exec -T postgres \
  psql -U opsintel -d opsintel \
  < sql/validation/raw_quality_summary.sql

echo "Database initialization complete."