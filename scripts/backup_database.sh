#!/usr/bin/env bash

set -euo pipefail

BACKUP_DIR="database/backups"
BACKUP_FILE="${BACKUP_DIR}/opsintel.dump"

mkdir -p "${BACKUP_DIR}"

echo "Creating PostgreSQL backup..."

docker compose exec -T postgres \
  pg_dump \
  -U opsintel \
  -d opsintel \
  -Fc \
  > "${BACKUP_FILE}"

echo "Backup created:"
ls -lh "${BACKUP_FILE}"