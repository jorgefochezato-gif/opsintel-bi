CREATE TABLE IF NOT EXISTS raw.shipments (
    shipment_id TEXT,
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
    created_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.transportation_costs (
    transportation_cost_id TEXT,
    shipment_id TEXT,
    cost_date DATE,
    cost_type TEXT,
    cost_amount NUMERIC(14, 2),
    currency TEXT,
    transaction_type TEXT,
    created_timestamp TIMESTAMP
);