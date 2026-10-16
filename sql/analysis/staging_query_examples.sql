-- OpsIntel BI
-- Representative staging queries

-- ---------------------------------------------------------
-- 1. Shipment volume by month
-- ---------------------------------------------------------

SELECT
    DATE_TRUNC(
        'month',
        shipment_date
    )::date AS shipment_month,
    COUNT(*) AS shipment_count,
    SUM(shipment_quantity) AS shipment_volume
FROM staging.shipments_clean
WHERE shipment_quantity IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------
-- 2. Carrier delivery performance
-- ---------------------------------------------------------

SELECT
    carrier_id,

    COUNT(*) FILTER (
        WHERE shipment_status = 'DELIVERED'
    ) AS delivered_shipments,

    COUNT(*) FILTER (
        WHERE shipment_status = 'DELIVERED'
          AND actual_delivery_date
              <= expected_delivery_date
    ) AS on_time_shipments,

    ROUND(
        100.0
        * COUNT(*) FILTER (
            WHERE shipment_status = 'DELIVERED'
              AND actual_delivery_date
                  <= expected_delivery_date
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE shipment_status = 'DELIVERED'
            ),
            0
        ),
        2
    ) AS on_time_percentage

FROM staging.shipments_clean

WHERE carrier_id IS NOT NULL

GROUP BY carrier_id

ORDER BY on_time_percentage DESC;

-- ---------------------------------------------------------
-- 3. Transportation cost by month
-- ---------------------------------------------------------

SELECT
    DATE_TRUNC(
        'month',
        cost_date
    )::date AS cost_month,

    SUM(cost_amount) AS total_transportation_cost,

    AVG(cost_amount) AS average_cost_transaction

FROM staging.transportation_costs_clean

GROUP BY 1

ORDER BY 1;

-- ---------------------------------------------------------
-- 4. Cost per shipment
-- ---------------------------------------------------------

SELECT
    s.shipment_id,
    s.carrier_id,
    s.route_id,
    SUM(c.cost_amount) AS total_transportation_cost

FROM staging.shipments_clean AS s

JOIN staging.transportation_costs_clean AS c
    ON c.shipment_id = s.shipment_id

GROUP BY
    s.shipment_id,
    s.carrier_id,
    s.route_id

ORDER BY total_transportation_cost DESC

LIMIT 100;