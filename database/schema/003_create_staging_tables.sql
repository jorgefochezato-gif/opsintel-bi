CREATE TABLE IF NOT EXISTS staging.shipments_clean (
    shipment_id TEXT PRIMARY KEY,
    customer_id TEXT,
    carrier_id TEXT,
    route_id TEXT,
    origin_location_id TEXT,
    destination_location_id TEXT,
    shipment_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    shipment_status TEXT,
    shipment_quantity INTEGER,
    transportation_mode TEXT,
    created_timestamp TIMESTAMP,
    quality_status TEXT NOT NULL,
    quality_notes TEXT
);

CREATE TABLE IF NOT EXISTS staging.transportation_costs_clean (
    transportation_cost_id TEXT PRIMARY KEY,
    shipment_id TEXT,
    cost_date DATE,
    cost_type TEXT,
    cost_amount NUMERIC(14, 2),
    currency TEXT,
    transaction_type TEXT,
    created_timestamp TIMESTAMP,
    quality_status TEXT NOT NULL,
    quality_notes TEXT
);