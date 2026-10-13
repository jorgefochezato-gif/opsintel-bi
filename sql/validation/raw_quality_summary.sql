SELECT
    'duplicate_shipments' AS check_name,
    COUNT(*) AS issue_count
FROM (
    SELECT shipment_id
    FROM raw.shipments
    GROUP BY shipment_id
    HAVING COUNT(*) > 1
) duplicate_shipments

UNION ALL

SELECT
    'missing_carriers',
    COUNT(*)
FROM raw.shipments
WHERE carrier_id IS NULL

UNION ALL

SELECT
    'invalid_quantities',
    COUNT(*)
FROM raw.shipments
WHERE shipment_quantity <= 0

UNION ALL

SELECT
    'invalid_delivery_dates',
    COUNT(*)
FROM raw.shipments
WHERE actual_delivery_date < shipment_date

UNION ALL

SELECT
    'negative_transportation_costs',
    COUNT(*)
FROM raw.transportation_costs
WHERE cost_amount < 0

ORDER BY check_name;