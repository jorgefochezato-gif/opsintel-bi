#!/usr/bin/env bash

set -euo pipefail

BACKUP_FILE="database/backups/opsintel.dump"
RESTORE_DB="opsintel_restore_test"

if [[ ! -f "${BACKUP_FILE}" ]]; then
  echo "Backup not found: ${BACKUP_FILE}"
  exit 1
fi

echo "Dropping previous restore-test database if it exists..."

docker compose exec -T postgres \
  psql -U opsintel -d postgres \
  -c "DROP DATABASE IF EXISTS ${RESTORE_DB};"

echo "Creating restore-test database..."

docker compose exec -T postgres \
  psql -U opsintel -d postgres \
  -c "CREATE DATABASE ${RESTORE_DB};"

echo "Restoring backup..."

cat "${BACKUP_FILE}" | \
docker compose exec -T postgres \
  pg_restore \
  -U opsintel \
  -d "${RESTORE_DB}" \
  --no-owner

echo "Validating restored database..."

docker compose exec -T postgres \
  psql -U opsintel -d "${RESTORE_DB}" \
  -c "
SELECT
    (SELECT COUNT(*) FROM raw.shipments) AS raw_shipments,
    (SELECT COUNT(*) FROM staging.shipments_clean) AS staging_shipments,
    (SELECT COUNT(*) FROM raw.transportation_costs) AS raw_costs,
    (SELECT COUNT(*) FROM staging.transportation_costs_clean) AS staging_costs;
"

echo "Restore verification complete."