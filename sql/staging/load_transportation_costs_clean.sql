TRUNCATE TABLE staging.transportation_costs_clean;

INSERT INTO staging.transportation_costs_clean (
    transportation_cost_id,
    shipment_id,
    cost_date,
    cost_type,
    cost_amount,
    currency,
    transaction_type,
    created_timestamp,
    quality_status,
    quality_notes
)

SELECT
    transportation_cost_id,
    shipment_id,
    cost_date,
    cost_type,
    cost_amount,
    currency,
    transaction_type,
    created_timestamp,

    CASE
        WHEN shipment_id IS NULL
        THEN 'WARNING'

        WHEN transaction_type IN ('CREDIT', 'REVERSAL')
             AND cost_amount > 0
        THEN 'WARNING'

        ELSE 'VALID'
    END AS quality_status,

    NULLIF(
        CONCAT_WS(
            '; ',
            CASE
                WHEN shipment_id IS NULL
                THEN 'Missing shipment reference'
            END,
            CASE
                WHEN transaction_type IN ('CREDIT', 'REVERSAL')
                     AND cost_amount > 0
                THEN 'Credit or reversal has positive amount'
            END
        ),
        ''
    ) AS quality_notes

FROM raw.transportation_costs;