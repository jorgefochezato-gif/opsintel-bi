-- OpsIntel BI
-- Raw shipment data-quality validation

-- 1. Total rows
SELECT
    COUNT(*) AS shipment_rows
FROM raw.shipments;

-- 2. Duplicate shipment IDs
SELECT
    shipment_id,
    COUNT(*) AS row_count
FROM raw.shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1
ORDER BY row_count DESC, shipment_id;

-- 3. Missing carrier references
SELECT
    COUNT(*) AS missing_carrier_rows
FROM raw.shipments
WHERE carrier_id IS NULL;

-- 4. Invalid shipment quantities
SELECT
    COUNT(*) AS invalid_quantity_rows
FROM raw.shipments
WHERE shipment_quantity <= 0;

-- 5. Invalid delivery date sequences
SELECT
    COUNT(*) AS invalid_delivery_date_rows
FROM raw.shipments
WHERE actual_delivery_date < shipment_date;

-- 6. Delivered shipments missing an actual delivery date
SELECT
    COUNT(*) AS delivered_missing_actual_date
FROM raw.shipments
WHERE shipment_status = 'DELIVERED'
  AND actual_delivery_date IS NULL;

-- 7. Non-delivered shipments with an actual delivery date
SELECT
    COUNT(*) AS unexpected_actual_delivery_date
FROM raw.shipments
WHERE shipment_status <> 'DELIVERED'
  AND actual_delivery_date IS NOT NULL;

-- 8. Shipment-status distribution
SELECT
    shipment_status,
    COUNT(*) AS row_count
FROM raw.shipments
GROUP BY shipment_status
ORDER BY row_count DESC;

-- 9. Transportation-mode distribution
SELECT
    transportation_mode,
    COUNT(*) AS row_count
FROM raw.shipments
GROUP BY transportation_mode
ORDER BY row_count DESC;

-- 10. Shipment date range
SELECT
    MIN(shipment_date) AS min_shipment_date,
    MAX(shipment_date) AS max_shipment_date
FROM raw.shipments;