from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Output directories
GENERATED_DATA_DIR = PROJECT_ROOT / "data" / "generated"

# Reproducibility
RANDOM_SEED = 42

# Historical reporting period
START_DATE = "2024-01-01"
END_DATE = "2026-12-31"

# Initial dataset sizes
REGION_COUNT = 3
LOCATION_COUNT = 80
CUSTOMER_COUNT = 300
CARRIER_COUNT = 20
ROUTE_COUNT = 300
ASSET_COUNT = 5000
SHIPMENT_COUNT = 100_000

# Controlled anomaly rates
DUPLICATE_SHIPMENT_RATE = 0.001
MISSING_CARRIER_RATE = 0.002
INVALID_DATE_RATE = 0.001
INVALID_QUANTITY_RATE = 0.001
COST_ANOMALY_RATE = 0.002