from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_generated(filename: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(
        GENERATED_DIR / filename,
        **kwargs,
    )


def load_raw(filename: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(
        RAW_DIR / filename,
        **kwargs,
    )


def test_regions() -> None:
    regions = load_generated("regions.csv")

    assert len(regions) == 3
    assert regions["region_id"].is_unique
    assert regions["region_name"].is_unique
    assert regions["region_id"].notna().all()
    assert regions["region_name"].notna().all()


def test_locations() -> None:
    regions = load_generated("regions.csv")
    locations = load_generated("locations.csv")

    assert len(locations) == 80
    assert locations["location_id"].is_unique

    assert locations["region_id"].isin(
        regions["region_id"]
    ).all()

    assert locations["latitude"].between(
        -90,
        90,
    ).all()

    assert locations["longitude"].between(
        -180,
        180,
    ).all()

    allowed_countries = {
        "REG-001": {"US", "CA", "MX"},
        "REG-002": {"BE", "DE", "FR", "ES", "NL"},
        "REG-003": {"AR", "BR", "CL", "CO", "PE"},
    }

    for region_id, countries in allowed_countries.items():
        subset = locations[
            locations["region_id"] == region_id
        ]

        assert subset["country_code"].isin(
            countries
        ).all()


def test_customers() -> None:
    customers = load_generated("customers.csv")
    regions = load_generated("regions.csv")

    assert len(customers) == 300
    assert customers["customer_id"].is_unique

    assert customers["region_id"].isin(
        regions["region_id"]
    ).all()

    valid_statuses = {
        "ACTIVE",
        "INACTIVE",
    }

    assert set(
        customers["customer_status"]
    ).issubset(valid_statuses)

    inactive = customers[
        customers["customer_status"] == "INACTIVE"
    ]

    active = customers[
        customers["customer_status"] == "ACTIVE"
    ]

    assert inactive["inactive_date"].notna().all()
    assert active["inactive_date"].isna().all()


def test_carriers() -> None:
    carriers = load_generated("carriers.csv")
    regions = load_generated("regions.csv")

    assert len(carriers) == 20
    assert carriers["carrier_id"].is_unique

    assert carriers["primary_region_id"].isin(
        regions["region_id"]
    ).all()

    assert carriers["cost_multiplier"].gt(0).all()

    assert carriers[
        "on_time_probability"
    ].between(
        0,
        1,
    ).all()

    assert carriers[
        "transit_time_multiplier"
    ].gt(0).all()


def test_routes() -> None:
    routes = load_generated("routes.csv")
    locations = load_generated("locations.csv")

    assert len(routes) == 300
    assert routes["route_id"].is_unique

    location_ids = set(
        locations["location_id"]
    )

    assert routes[
        "origin_location_id"
    ].isin(location_ids).all()

    assert routes[
        "destination_location_id"
    ].isin(location_ids).all()

    assert (
        routes["origin_location_id"]
        != routes["destination_location_id"]
    ).all()

    assert routes["distance_km"].gt(0).all()

    assert routes[
        "expected_transit_days"
    ].gt(0).all()

    duplicates = routes.duplicated(
        subset=[
            "origin_location_id",
            "destination_location_id",
        ]
    )

    assert not duplicates.any()


def test_assets() -> None:
    assets = load_generated("assets.csv")
    locations = load_generated("locations.csv")

    assert len(assets) == 5000
    assert assets["asset_id"].is_unique

    location_ids = set(
        locations["location_id"]
    )

    assert assets[
        "home_location_id"
    ].isin(location_ids).all()

    assert assets[
        "current_location_id"
    ].isin(location_ids).all()

    retired = assets[
        assets["asset_status"] == "RETIRED"
    ]

    not_retired = assets[
        assets["asset_status"] != "RETIRED"
    ]

    assert retired[
        "retirement_date"
    ].notna().all()

    assert not_retired[
        "retirement_date"
    ].isna().all()


def test_shipments() -> None:
    shipments = load_generated(
        "shipments.csv",
        parse_dates=[
            "shipment_date",
            "expected_delivery_date",
            "actual_delivery_date",
        ],
    )

    customers = load_generated("customers.csv")
    carriers = load_generated("carriers.csv")
    routes = load_generated("routes.csv")
    locations = load_generated("locations.csv")

    assert len(shipments) == 100_000

    assert shipments[
        "shipment_id"
    ].is_unique

    assert shipments[
        "customer_id"
    ].isin(
        customers["customer_id"]
    ).all()

    assert shipments[
        "carrier_id"
    ].isin(
        carriers["carrier_id"]
    ).all()

    assert shipments[
        "route_id"
    ].isin(
        routes["route_id"]
    ).all()

    assert shipments[
        "origin_location_id"
    ].isin(
        locations["location_id"]
    ).all()

    assert shipments[
        "destination_location_id"
    ].isin(
        locations["location_id"]
    ).all()

    assert shipments[
        "shipment_quantity"
    ].gt(0).all()

    delivered = shipments[
        shipments["shipment_status"] == "DELIVERED"
    ]

    not_delivered = shipments[
        shipments["shipment_status"] != "DELIVERED"
    ]

    assert delivered[
        "actual_delivery_date"
    ].notna().all()

    assert not_delivered[
        "actual_delivery_date"
    ].isna().all()

    assert (
        delivered["actual_delivery_date"]
        >= delivered["shipment_date"]
    ).all()


def test_transportation_costs() -> None:
    shipments = load_generated("shipments.csv")
    costs = load_generated(
        "transportation_costs.csv"
    )

    assert len(costs) > len(shipments)

    assert costs[
        "transportation_cost_id"
    ].is_unique

    assert costs[
        "shipment_id"
    ].isin(
        shipments["shipment_id"]
    ).all()

    base_freight = costs[
        costs["cost_type"] == "BASE_FREIGHT"
    ]

    credits = costs[
        costs["transaction_type"] == "CREDIT"
    ]

    assert base_freight[
        "cost_amount"
    ].gt(0).all()

    assert credits[
        "cost_amount"
    ].lt(0).all()


def test_transportation_budgets() -> None:
    budgets = load_generated(
        "transportation_budgets.csv",
        parse_dates=["budget_month"],
    )

    regions = load_generated("regions.csv")

    expected_months = pd.date_range(
        start="2024-01-01",
        end="2026-09-30",
        freq="MS",
    )

    expected_rows = (
        len(expected_months)
        * len(regions)
    )

    assert len(budgets) == expected_rows

    assert budgets[
        "budget_id"
    ].is_unique

    duplicates = budgets.duplicated(
        subset=[
            "budget_month",
            "region_id",
        ]
    )

    assert not duplicates.any()

    assert budgets[
        "budget_amount"
    ].ge(0).all()


def test_asset_movements() -> None:
    movements = load_generated(
        "asset_movements.csv",
        parse_dates=[
            "movement_timestamp",
        ],
    )

    assets = load_generated("assets.csv")
    locations = load_generated("locations.csv")
    shipments = load_generated("shipments.csv")

    assert len(movements) > 100_000

    assert movements[
        "asset_movement_id"
    ].is_unique

    assert movements[
        "asset_id"
    ].isin(
        assets["asset_id"]
    ).all()

    assert (
        movements["origin_location_id"]
        .dropna()
        .isin(
            locations["location_id"]
        )
        .all()
    )

    assert (
        movements["destination_location_id"]
        .dropna()
        .isin(
            locations["location_id"]
        )
        .all()
    )

    assert (
        movements["related_shipment_id"]
        .dropna()
        .isin(
            shipments["shipment_id"]
        )
        .all()
    )


def test_operational_exceptions() -> None:
    exceptions = load_generated(
        "operational_exceptions.csv",
        parse_dates=[
            "exception_date",
            "resolution_date",
        ],
    )

    shipments = load_generated("shipments.csv")
    assets = load_generated("assets.csv")
    locations = load_generated("locations.csv")

    assert len(exceptions) > 5_000

    assert exceptions[
        "exception_id"
    ].is_unique

    assert (
        exceptions["shipment_id"]
        .dropna()
        .isin(
            shipments["shipment_id"]
        )
        .all()
    )

    assert (
        exceptions["asset_id"]
        .dropna()
        .isin(
            assets["asset_id"]
        )
        .all()
    )

    assert (
        exceptions["location_id"]
        .dropna()
        .isin(
            locations["location_id"]
        )
        .all()
    )

    resolved = exceptions[
        exceptions["resolved_flag"]
    ]

    assert resolved[
        "resolution_date"
    ].notna().all()


def test_raw_source_defects_exist() -> None:
    clean_shipments = load_generated(
        "shipments.csv"
    )

    raw_shipments = load_raw(
        "shipments.csv"
    )

    clean_costs = load_generated(
        "transportation_costs.csv"
    )

    raw_costs = load_raw(
        "transportation_costs.csv"
    )

    issues = load_generated(
        "data_quality_issues.csv"
    )

    assert len(raw_shipments) > len(
        clean_shipments
    )

    assert raw_shipments[
        "carrier_id"
    ].isna().sum() > 0

    assert raw_shipments[
        "shipment_quantity"
    ].le(0).sum() > 0

    raw_dates = raw_shipments.copy()

    raw_dates["shipment_date"] = pd.to_datetime(
        raw_dates["shipment_date"]
    )

    raw_dates[
        "actual_delivery_date"
    ] = pd.to_datetime(
        raw_dates[
            "actual_delivery_date"
        ]
    )

    invalid_dates = (
        raw_dates[
            "actual_delivery_date"
        ]
        < raw_dates[
            "shipment_date"
        ]
    ).fillna(False)

    assert invalid_dates.any()

    assert raw_costs[
        "cost_amount"
    ].max() > clean_costs[
        "cost_amount"
    ].max()

    assert len(issues) > 0