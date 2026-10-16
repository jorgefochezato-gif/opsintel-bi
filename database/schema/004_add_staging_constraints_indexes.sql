-- OpsIntel BI
-- Staging constraints and indexes

-- ---------------------------------------------------------
-- Shipments
-- ---------------------------------------------------------

ALTER TABLE staging.shipments_clean
    ALTER COLUMN shipment_id SET NOT NULL;

ALTER TABLE staging.shipments_clean
    ADD CONSTRAINT shipments_clean_status_check
    CHECK (
        shipment_status IN (
            'PLANNED',
            'IN_TRANSIT',
            'DELIVERED',
            'CANCELLED'
        )
    );

ALTER TABLE staging.shipments_clean
    ADD CONSTRAINT shipments_clean_quality_status_check
    CHECK (
        quality_status IN (
            'VALID',
            'WARNING'
        )
    );

CREATE INDEX IF NOT EXISTS idx_shipments_clean_shipment_date
    ON staging.shipments_clean (shipment_date);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_customer
    ON staging.shipments_clean (customer_id);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_carrier
    ON staging.shipments_clean (carrier_id);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_route
    ON staging.shipments_clean (route_id);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_status
    ON staging.shipments_clean (shipment_status);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_origin
    ON staging.shipments_clean (origin_location_id);

CREATE INDEX IF NOT EXISTS idx_shipments_clean_destination
    ON staging.shipments_clean (destination_location_id);

-- Useful for common date + status analysis
CREATE INDEX IF NOT EXISTS idx_shipments_clean_date_status
    ON staging.shipments_clean (
        shipment_date,
        shipment_status
    );

-- ---------------------------------------------------------
-- Transportation costs
-- ---------------------------------------------------------

ALTER TABLE staging.transportation_costs_clean
    ALTER COLUMN transportation_cost_id SET NOT NULL;

ALTER TABLE staging.transportation_costs_clean
    ADD CONSTRAINT transportation_costs_quality_status_check
    CHECK (
        quality_status IN (
            'VALID',
            'WARNING'
        )
    );

ALTER TABLE staging.transportation_costs_clean
    ADD CONSTRAINT transportation_costs_transaction_type_check
    CHECK (
        transaction_type IN (
            'CHARGE',
            'CREDIT',
            'REVERSAL'
        )
    );

CREATE INDEX IF NOT EXISTS idx_transportation_costs_shipment
    ON staging.transportation_costs_clean (shipment_id);

CREATE INDEX IF NOT EXISTS idx_transportation_costs_date
    ON staging.transportation_costs_clean (cost_date);

CREATE INDEX IF NOT EXISTS idx_transportation_costs_type
    ON staging.transportation_costs_clean (cost_type);

CREATE INDEX IF NOT EXISTS idx_transportation_costs_transaction_type
    ON staging.transportation_costs_clean (transaction_type);

CREATE INDEX IF NOT EXISTS idx_transportation_costs_shipment_date
    ON staging.transportation_costs_clean (
        shipment_id,
        cost_date
    );