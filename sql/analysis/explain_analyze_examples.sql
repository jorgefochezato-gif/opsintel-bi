-- OpsIntel BI
-- Query execution-plan examples

-- ---------------------------------------------------------
-- Example 1
-- Filter shipments by carrier
-- ---------------------------------------------------------

EXPLAIN (
    ANALYZE,
    BUFFERS
)

SELECT
    shipment_id,
    shipment_date,
    shipment_status
FROM staging.shipments_clean
WHERE carrier_id = 'CAR-0001';


-- ---------------------------------------------------------
-- Example 2
-- Filter shipments by date range
-- ---------------------------------------------------------

EXPLAIN (
    ANALYZE,
    BUFFERS
)

SELECT
    COUNT(*)
FROM staging.shipments_clean
WHERE shipment_date
    BETWEEN DATE '2026-01-01'
    AND DATE '2026-09-30';


-- ---------------------------------------------------------
-- Example 3
-- Shipment-to-cost join
-- ---------------------------------------------------------

EXPLAIN (
    ANALYZE,
    BUFFERS
)

SELECT
    s.carrier_id,
    SUM(c.cost_amount) AS total_cost

FROM staging.shipments_clean AS s

JOIN staging.transportation_costs_clean AS c
    ON c.shipment_id = s.shipment_id

WHERE s.shipment_date
    BETWEEN DATE '2026-01-01'
    AND DATE '2026-09-30'

GROUP BY s.carrier_id;