TRUNCATE TABLE staging.shipments_clean;

WITH ranked_shipments AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY shipment_id
            ORDER BY created_timestamp ASC
        ) AS duplicate_rank
    FROM raw.shipments
),

classified_shipments AS (
    SELECT
        shipment_id,
        customer_id,
        carrier_id,
        route_id,
        origin_location_id,
        destination_location_id,
        shipment_date,
        expected_delivery_date,

        CASE
            WHEN actual_delivery_date < shipment_date
                THEN NULL
            ELSE actual_delivery_date
        END AS actual_delivery_date,

        shipment_status,

        CASE
            WHEN shipment_quantity <= 0
                THEN NULL
            ELSE shipment_quantity
        END AS shipment_quantity,

        transportation_mode,
        created_timestamp,

        CASE
            WHEN carrier_id IS NULL
              OR shipment_quantity <= 0
              OR actual_delivery_date < shipment_date
            THEN 'WARNING'
            ELSE 'VALID'
        END AS quality_status,

        CONCAT_WS(
            '; ',
            CASE
                WHEN carrier_id IS NULL
                THEN 'Missing carrier reference'
            END,
            CASE
                WHEN shipment_quantity <= 0
                THEN 'Invalid shipment quantity'
            END,
            CASE
                WHEN actual_delivery_date < shipment_date
                THEN 'Actual delivery date precedes shipment date'
            END
        ) AS quality_notes

    FROM ranked_shipments

    WHERE duplicate_rank = 1
)

INSERT INTO staging.shipments_clean (
    shipment_id,
    customer_id,
    carrier_id,
    route_id,
    origin_location_id,
    destination_location_id,
    shipment_date,
    expected_delivery_date,
    actual_delivery_date,
    shipment_status,
    shipment_quantity,
    transportation_mode,
    created_timestamp,
    quality_status,
    quality_notes
)

SELECT
    shipment_id,
    customer_id,
    carrier_id,
    route_id,
    origin_location_id,
    destination_location_id,
    shipment_date,
    expected_delivery_date,
    actual_delivery_date,
    shipment_status,
    shipment_quantity,
    transportation_mode,
    created_timestamp,
    quality_status,
    NULLIF(quality_notes, '')
FROM classified_shipments;