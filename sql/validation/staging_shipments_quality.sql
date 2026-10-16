-- OpsIntel BI
-- Staging shipment validation

-- 1. Total staged shipment rows
SELECT
    COUNT(*) AS staging_shipment_rows
FROM staging.shipments_clean;

-- 2. Duplicate shipment IDs should not exist
SELECT
    COUNT(*) AS duplicate_shipment_ids
FROM (
    SELECT shipment_id
    FROM staging.shipments_clean
    GROUP BY shipment_id
    HAVING COUNT(*) > 1
) duplicates;

-- 3. Invalid quantities should have been normalized to NULL
SELECT
    COUNT(*) AS remaining_nonpositive_quantities
FROM staging.shipments_clean
WHERE shipment_quantity <= 0;

-- 4. Invalid delivery date sequences should no longer exist
SELECT
    COUNT(*) AS remaining_invalid_delivery_dates
FROM staging.shipments_clean
WHERE actual_delivery_date < shipment_date;

-- 5. Missing carriers are preserved and flagged
SELECT
    COUNT(*) AS missing_carrier_rows
FROM staging.shipments_clean
WHERE carrier_id IS NULL;

-- 6. Warning distribution
SELECT
    quality_status,
    COUNT(*) AS row_count
FROM staging.shipments_clean
GROUP BY quality_status
ORDER BY quality_status;

-- 7. Warning reasons
SELECT
    quality_notes,
    COUNT(*) AS row_count
FROM staging.shipments_clean
WHERE quality_status = 'WARNING'
GROUP BY quality_notes
ORDER BY row_count DESC, quality_notes;

-- 8. Delivered shipment rules
SELECT
    COUNT(*) AS delivered_without_actual_date
FROM staging.shipments_clean
WHERE shipment_status = 'DELIVERED'
  AND actual_delivery_date IS NULL
  AND quality_notes IS DISTINCT FROM
      'Actual delivery date precedes shipment date';

-- 9. Shipment date range
SELECT
    MIN(shipment_date) AS min_shipment_date,
    MAX(shipment_date) AS max_shipment_date
FROM staging.shipments_clean;