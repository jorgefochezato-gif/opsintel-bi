import random

import numpy as np
import pandas as pd
from faker import Faker
from math import asin, cos, radians, sin, sqrt

from config import (
    ASSET_COUNT,
    CARRIER_COUNT,
    COST_ANOMALY_RATE,
    CUSTOMER_COUNT,
    DUPLICATE_SHIPMENT_RATE,
    END_DATE,
    GENERATED_DATA_DIR,
    INVALID_DATE_RATE,
    INVALID_QUANTITY_RATE,
    LOCATION_COUNT,
    MISSING_CARRIER_RATE,
    RANDOM_SEED,
    RAW_DATA_DIR,
    ROUTE_COUNT,
    SHIPMENT_COUNT,
    START_DATE,
)


def initialize_random_state() -> Faker:
    """
    Initialize all pseudo-random generators using the same deterministic seed.
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    faker = Faker()
    faker.seed_instance(RANDOM_SEED)

    return faker


def ensure_output_directories() -> None:
    """
    Ensure all generated-data output directories exist.
    """
    GENERATED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def generate_regions() -> pd.DataFrame:
    """
    Generate the fixed enterprise operating regions.
    """
    regions = [
        {
            "region_id": "REG-001",
            "region_name": "North America",
        },
        {
            "region_id": "REG-002",
            "region_name": "Europe",
        },
        {
            "region_id": "REG-003",
            "region_name": "Latin America",
        },
    ]

    return pd.DataFrame(regions)


def generate_locations(faker: Faker, regions: pd.DataFrame) -> pd.DataFrame:
    """
    Generate deterministic operational locations using coherent geographic data.
    """

    location_types = [
        "PLANT",
        "WAREHOUSE",
        "SERVICE_CENTER",
        "CUSTOMER_SITE",
        "PORT",
    ]

    geography_catalog = {
        "REG-001": [
            ("Orlando", "Florida", "United States", "US", 28.5383, -81.3792),
            ("Atlanta", "Georgia", "United States", "US", 33.7490, -84.3880),
            ("Dallas", "Texas", "United States", "US", 32.7767, -96.7970),
            ("Chicago", "Illinois", "United States", "US", 41.8781, -87.6298),
            ("Los Angeles", "California", "United States", "US", 34.0522, -118.2437),
            ("Toronto", "Ontario", "Canada", "CA", 43.6532, -79.3832),
            ("Montreal", "Quebec", "Canada", "CA", 45.5017, -73.5673),
            ("Vancouver", "British Columbia", "Canada", "CA", 49.2827, -123.1207),
            ("Monterrey", "Nuevo Leon", "Mexico", "MX", 25.6866, -100.3161),
            ("Mexico City", "CDMX", "Mexico", "MX", 19.4326, -99.1332),
        ],
        "REG-002": [
            ("Brussels", "Brussels-Capital", "Belgium", "BE", 50.8503, 4.3517),
            ("Antwerp", "Antwerp", "Belgium", "BE", 51.2194, 4.4025),
            ("Berlin", "Berlin", "Germany", "DE", 52.5200, 13.4050),
            ("Hamburg", "Hamburg", "Germany", "DE", 53.5511, 9.9937),
            ("Paris", "Ile-de-France", "France", "FR", 48.8566, 2.3522),
            ("Lyon", "Auvergne-Rhone-Alpes", "France", "FR", 45.7640, 4.8357),
            ("Madrid", "Community of Madrid", "Spain", "ES", 40.4168, -3.7038),
            ("Barcelona", "Catalonia", "Spain", "ES", 41.3874, 2.1686),
            ("Amsterdam", "North Holland", "Netherlands", "NL", 52.3676, 4.9041),
            ("Rotterdam", "South Holland", "Netherlands", "NL", 51.9244, 4.4777),
        ],
        "REG-003": [
            ("Buenos Aires", "Buenos Aires", "Argentina", "AR", -34.6037, -58.3816),
            ("Cordoba", "Cordoba", "Argentina", "AR", -31.4201, -64.1888),
            ("Sao Paulo", "Sao Paulo", "Brazil", "BR", -23.5505, -46.6333),
            ("Rio de Janeiro", "Rio de Janeiro", "Brazil", "BR", -22.9068, -43.1729),
            ("Santiago", "Santiago Metropolitan", "Chile", "CL", -33.4489, -70.6693),
            ("Valparaiso", "Valparaiso", "Chile", "CL", -33.0472, -71.6127),
            ("Bogota", "Bogota", "Colombia", "CO", 4.7110, -74.0721),
            ("Medellin", "Antioquia", "Colombia", "CO", 6.2442, -75.5812),
            ("Lima", "Lima", "Peru", "PE", -12.0464, -77.0428),
            ("Arequipa", "Arequipa", "Peru", "PE", -16.4090, -71.5375),
        ],
    }

    locations = []
    region_ids = regions["region_id"].tolist()

    for index in range(1, LOCATION_COUNT + 1):
        region_id = random.choice(region_ids)

        (
            city,
            state_province,
            country,
            country_code,
            base_latitude,
            base_longitude,
        ) = random.choice(geography_catalog[region_id])

        location_type = random.choice(location_types)

        # Add a very small coordinate offset so multiple operational sites
        # can exist around the same metropolitan area.
        latitude = round(base_latitude + random.uniform(-0.08, 0.08), 6)
        longitude = round(base_longitude + random.uniform(-0.08, 0.08), 6)

        location_id = f"LOC-{index:04d}"
        site_suffix = faker.bothify(text="??-###").upper()

        locations.append(
            {
                "location_id": location_id,
                "location_name": (
                    f"{city} {location_type.replace('_', ' ').title()} {site_suffix}"
                ),
                "location_type": location_type,
                "city": city,
                "state_province": state_province,
                "country": country,
                "country_code": country_code,
                "region_id": region_id,
                "latitude": latitude,
                "longitude": longitude,
                "active_flag": random.random() > 0.05,
            }
        )

    return pd.DataFrame(locations)


def generate_customers(
    faker: Faker,
    regions: pd.DataFrame,
    customer_count: int,
 ) -> pd.DataFrame:
    """
    Generate enterprise customers assigned to operating regions.
    """

    customer_segments = [
        "ENTERPRISE",
        "MID_MARKET",
        "SMALL_BUSINESS",
        "STRATEGIC",
    ]

    region_ids = regions["region_id"].tolist()

    customers = []

    for index in range(1, customer_count + 1):
        customer_id = f"CUS-{index:05d}"

        region_id = random.choice(region_ids)
        status = "ACTIVE" if random.random() > 0.08 else "INACTIVE"

        created_date = faker.date_between(
            start_date="-8y",
            end_date="-3y",
        )

        inactive_date = None

        if status == "INACTIVE":
            inactive_date = faker.date_between(
                start_date="-2y",
                end_date="today",
            )

        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": faker.company(),
                "customer_status": status,
                "customer_segment": random.choice(customer_segments),
                "region_id": region_id,
                "created_date": created_date,
                "inactive_date": inactive_date,
            }
        )

    return pd.DataFrame(customers)


def generate_carriers(
    faker: Faker,
    regions: pd.DataFrame,
    carrier_count: int,
) -> pd.DataFrame:
    """
    Generate transportation carriers with deterministic business characteristics.

    Cost and service profile fields will later influence shipment cost,
    transit time, and delivery reliability.
    """

    transportation_modes = [
        "TRUCK",
        "RAIL",
        "AIR",
        "OCEAN",
        "INTERMODAL",
    ]

    service_profiles = {
        "PREMIUM": {
            "cost_multiplier": 1.25,
            "on_time_probability": 0.96,
            "transit_time_multiplier": 0.85,
        },
        "STANDARD": {
            "cost_multiplier": 1.00,
            "on_time_probability": 0.90,
            "transit_time_multiplier": 1.00,
        },
        "ECONOMY": {
            "cost_multiplier": 0.82,
            "on_time_probability": 0.82,
            "transit_time_multiplier": 1.15,
        },
    }

    service_profile_names = list(service_profiles.keys())
    region_ids = regions["region_id"].tolist()

    carriers = []

    for index in range(1, carrier_count + 1):
        carrier_id = f"CAR-{index:04d}"
        service_profile = random.choice(service_profile_names)
        profile = service_profiles[service_profile]

        carrier_status = "ACTIVE" if random.random() > 0.10 else "INACTIVE"

        carriers.append(
            {
                "carrier_id": carrier_id,
                "carrier_name": f"{faker.company()} Logistics",
                "carrier_status": carrier_status,
                "transportation_mode": random.choice(transportation_modes),
                "primary_region_id": random.choice(region_ids),
                "service_profile": service_profile,
                "cost_multiplier": profile["cost_multiplier"],
                "on_time_probability": profile["on_time_probability"],
                "transit_time_multiplier": profile["transit_time_multiplier"],
                "created_date": faker.date_between(
                    start_date="-10y",
                    end_date="-3y",
                ),
            }
        )

    return pd.DataFrame(carriers)


def write_dataset(
    df: pd.DataFrame,
    filename: str,
    output_directory=GENERATED_DATA_DIR,
) -> None:
    """
    Write a dataset to the selected output directory.
    """
    output_path = output_directory / filename

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Wrote {len(df):,} rows -> {output_path}"
    )


def haversine_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate approximate great-circle distance between two coordinates.
    """
    earth_radius_km = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad)
        * cos(lat2_rad)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return earth_radius_km * c


def generate_routes(
    locations: pd.DataFrame,
    route_count: int,
) -> pd.DataFrame:
    """
    Generate unique origin-to-destination transportation routes.
    """

    mode_speed_km_per_day = {
        "TRUCK": 650,
        "RAIL": 800,
        "AIR": 5000,
        "OCEAN": 700,
        "INTERMODAL": 600,
    }

    active_locations = locations[locations["active_flag"]].copy()

    routes = []
    used_pairs = set()

    while len(routes) < route_count:
        origin = active_locations.sample(1).iloc[0]
        destination = active_locations.sample(1).iloc[0]

        if origin["location_id"] == destination["location_id"]:
            continue

        route_key = (
            origin["location_id"],
            destination["location_id"],
        )

        if route_key in used_pairs:
            continue

        used_pairs.add(route_key)

        distance_km = haversine_distance_km(
            origin["latitude"],
            origin["longitude"],
            destination["latitude"],
            destination["longitude"],
        )

        same_region = origin["region_id"] == destination["region_id"]

        if same_region:
            possible_modes = ["TRUCK", "RAIL", "INTERMODAL"]
        else:
            possible_modes = ["AIR", "OCEAN", "INTERMODAL"]

        transportation_mode = random.choice(possible_modes)

        expected_transit_days = max(
            1,
            round(
                distance_km
                / mode_speed_km_per_day[transportation_mode]
            ),
        )

        route_id = f"RTE-{len(routes) + 1:05d}"

        routes.append(
            {
                "route_id": route_id,
                "origin_location_id": origin["location_id"],
                "destination_location_id": destination["location_id"],
                "distance_km": round(distance_km, 1),
                "distance_unit": "KM",
                "expected_transit_days": expected_transit_days,
                "transportation_mode": transportation_mode,
                "active_flag": random.random() > 0.05,
            }
        )

    return pd.DataFrame(routes)


def generate_assets(
    faker: Faker,
    locations: pd.DataFrame,
    asset_count: int,
) -> pd.DataFrame:
    """
    Generate reusable logistics assets with lifecycle and location attributes.
    """

    asset_types = [
        "PALLET",
        "CONTAINER",
        "CRATE",
        "TOTE",
        "RACK",
    ]

    asset_statuses = [
        "AVAILABLE",
        "IN_USE",
        "IN_TRANSIT",
        "MAINTENANCE",
        "LOST",
        "RETIRED",
    ]

    status_weights = [
        0.42,  # AVAILABLE
        0.22,  # IN_USE
        0.20,  # IN_TRANSIT
        0.08,  # MAINTENANCE
        0.03,  # LOST
        0.05,  # RETIRED
    ]

    active_locations = locations[locations["active_flag"]].copy()

    assets = []

    for index in range(1, asset_count + 1):
        asset_id = f"AST-{index:06d}"

        home_location = active_locations.sample(1).iloc[0]
        current_location = active_locations.sample(1).iloc[0]

        asset_status = random.choices(
            asset_statuses,
            weights=status_weights,
            k=1,
        )[0]

        created_date = faker.date_between(
            start_date="-8y",
            end_date="-1y",
        )

        retirement_date = None

        if asset_status == "RETIRED":
            retirement_date = faker.date_between(
                start_date=created_date,
                end_date="today",
            )

        assets.append(
            {
                "asset_id": asset_id,
                "asset_type": random.choice(asset_types),
                "asset_status": asset_status,
                "home_location_id": home_location["location_id"],
                "current_location_id": current_location["location_id"],
                "created_date": created_date,
                "retirement_date": retirement_date,
            }
        )

    return pd.DataFrame(assets)


def generate_shipments(
    faker: Faker,
    customers: pd.DataFrame,
    carriers: pd.DataFrame,
    routes: pd.DataFrame,
    locations: pd.DataFrame,
    shipment_count: int,
) -> pd.DataFrame:
    """
    Generate shipment transactions using customer, carrier, route,
    service-level, and date behavior.

    Carrier service profiles influence delivery reliability and transit time.
    """

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)

    date_range_days = (end_date - start_date).days

    location_region_lookup = (
        locations
        .set_index("location_id")["region_id"]
        .to_dict()
    )

    active_customers = customers[
        customers["customer_status"] == "ACTIVE"
    ].copy()

    active_carriers = carriers[
        carriers["carrier_status"] == "ACTIVE"
    ].copy()

    active_routes = routes[
        routes["active_flag"]
    ].copy()

    shipments = []

    for index in range(1, shipment_count + 1):
        shipment_id = f"SHP-{index:07d}"

        route = active_routes.sample(1).iloc[0]

        origin_location_id = route["origin_location_id"]
        destination_location_id = route["destination_location_id"]

        origin_region_id = location_region_lookup[origin_location_id]

        # Prefer customers associated with the shipment's origin region.
        regional_customers = active_customers[
            active_customers["region_id"] == origin_region_id
        ]

        if regional_customers.empty:
            customer = active_customers.sample(1).iloc[0]
        else:
            customer = regional_customers.sample(1).iloc[0]

        # Prefer carriers whose transportation mode matches the route.
        compatible_carriers = active_carriers[
            active_carriers["transportation_mode"]
            == route["transportation_mode"]
        ]

        if compatible_carriers.empty:
            carrier = active_carriers.sample(1).iloc[0]
        else:
            carrier = compatible_carriers.sample(1).iloc[0]

        shipment_date = start_date + pd.Timedelta(
            days=random.randint(0, date_range_days)
        )

        expected_transit_days = int(
            route["expected_transit_days"]
        )

        expected_delivery_date = (
            shipment_date
            + pd.Timedelta(days=expected_transit_days)
        )

        status_roll = random.random()

        if status_roll < 0.92:
            shipment_status = "DELIVERED"
        elif status_roll < 0.96:
            shipment_status = "CANCELLED"
        elif status_roll < 0.985:
            shipment_status = "IN_TRANSIT"
        else:
            shipment_status = "PLANNED"

        actual_delivery_date = None

        if shipment_status == "DELIVERED":
            on_time_probability = float(
                carrier["on_time_probability"]
            )

            transit_multiplier = float(
                carrier["transit_time_multiplier"]
            )

            baseline_days = max(
                1,
                round(
                    expected_transit_days
                    * transit_multiplier
                ),
            )

            if random.random() <= on_time_probability:
                # Delivered on time.
                actual_transit_days = min(
                    expected_transit_days,
                    max(
                        1,
                        baseline_days
                        + random.randint(-1, 0),
                    ),
                )
            else:
                # Late delivery.
                late_days = random.randint(1, 5)

                actual_transit_days = max(
                    expected_transit_days + late_days,
                    baseline_days + late_days,
                )

            actual_delivery_date = (
                shipment_date
                + pd.Timedelta(days=actual_transit_days)
            )

        shipment_quantity = max(
            1,
            int(
                np.random.lognormal(
                    mean=3.2,
                    sigma=0.65,
                )
            ),
        )

        created_timestamp = (
            shipment_date
            - pd.Timedelta(
                days=random.randint(0, 7)
            )
            + pd.Timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
        )

        shipments.append(
            {
                "shipment_id": shipment_id,
                "customer_id": customer["customer_id"],
                "carrier_id": carrier["carrier_id"],
                "route_id": route["route_id"],
                "origin_location_id": origin_location_id,
                "destination_location_id": destination_location_id,
                "shipment_date": shipment_date.date(),
                "expected_delivery_date": (
                    expected_delivery_date.date()
                ),
                "actual_delivery_date": (
                    actual_delivery_date.date()
                    if actual_delivery_date is not None
                    else None
                ),
                "shipment_status": shipment_status,
                "shipment_quantity": shipment_quantity,
                "transportation_mode": route[
                    "transportation_mode"
                ],
                "created_timestamp": created_timestamp,
            }
        )

    return pd.DataFrame(shipments)


def generate_transportation_costs(
    shipments: pd.DataFrame,
    carriers: pd.DataFrame,
    routes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate transportation cost transactions associated with shipments.

    Cost behavior is influenced by:
    - route distance
    - transportation mode
    - shipment quantity
    - carrier cost profile

    A shipment may contain multiple cost transactions.
    """

    mode_base_rate_per_km = {
        "TRUCK": 1.20,
        "RAIL": 0.75,
        "AIR": 3.80,
        "OCEAN": 0.45,
        "INTERMODAL": 0.95,
    }

    carrier_lookup = (
        carriers
        .set_index("carrier_id")
        [
            [
                "cost_multiplier",
                "service_profile",
            ]
        ]
        .to_dict("index")
    )

    route_lookup = (
        routes
        .set_index("route_id")
        [
            [
                "distance_km",
                "transportation_mode",
            ]
        ]
        .to_dict("index")
    )

    cost_records = []
    cost_index = 1

    for shipment in shipments.itertuples(index=False):
        if shipment.shipment_status == "CANCELLED":
            continue

        route = route_lookup[shipment.route_id]
        carrier = carrier_lookup[shipment.carrier_id]

        distance_km = float(route["distance_km"])
        transportation_mode = route["transportation_mode"]

        quantity = int(shipment.shipment_quantity)

        base_rate = mode_base_rate_per_km[
            transportation_mode
        ]

        quantity_factor = max(
            1.0,
            quantity ** 0.45,
        )

        base_freight = (
            distance_km
            * base_rate
            * quantity_factor
            * float(carrier["cost_multiplier"])
        )

        # Add modest deterministic-looking commercial variation.
        base_freight *= random.uniform(0.92, 1.08)

        base_freight = max(
            25.0,
            round(base_freight, 2),
        )

        shipment_date = pd.Timestamp(
            shipment.shipment_date
        )

        cost_records.append(
            {
                "transportation_cost_id": (
                    f"CST-{cost_index:08d}"
                ),
                "shipment_id": shipment.shipment_id,
                "cost_date": shipment_date.date(),
                "cost_type": "BASE_FREIGHT",
                "cost_amount": base_freight,
                "currency": "USD",
                "transaction_type": "CHARGE",
                "created_timestamp": (
                    shipment_date
                    + pd.Timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59),
                    )
                ),
            }
        )

        cost_index += 1

        # Fuel surcharge is common but not universal.
        if random.random() < 0.88:
            fuel_rate = random.uniform(
                0.08,
                0.20,
            )

            fuel_surcharge = round(
                base_freight * fuel_rate,
                2,
            )

            cost_records.append(
                {
                    "transportation_cost_id": (
                        f"CST-{cost_index:08d}"
                    ),
                    "shipment_id": shipment.shipment_id,
                    "cost_date": shipment_date.date(),
                    "cost_type": "FUEL_SURCHARGE",
                    "cost_amount": fuel_surcharge,
                    "currency": "USD",
                    "transaction_type": "CHARGE",
                    "created_timestamp": (
                        shipment_date
                        + pd.Timedelta(
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                        )
                    ),
                }
            )

            cost_index += 1

        # Some shipments generate accessorial charges.
        if random.random() < 0.18:
            accessorial_charge = round(
                random.uniform(30, 350),
                2,
            )

            cost_records.append(
                {
                    "transportation_cost_id": (
                        f"CST-{cost_index:08d}"
                    ),
                    "shipment_id": shipment.shipment_id,
                    "cost_date": shipment_date.date(),
                    "cost_type": "ACCESSORIAL",
                    "cost_amount": accessorial_charge,
                    "currency": "USD",
                    "transaction_type": "CHARGE",
                    "created_timestamp": (
                        shipment_date
                        + pd.Timedelta(
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                        )
                    ),
                }
            )

            cost_index += 1

        # Toll charges occur mainly on ground transportation.
        if (
            transportation_mode
            in {"TRUCK", "INTERMODAL"}
            and random.random() < 0.30
        ):
            toll_charge = round(
                random.uniform(10, 180),
                2,
            )

            cost_records.append(
                {
                    "transportation_cost_id": (
                        f"CST-{cost_index:08d}"
                    ),
                    "shipment_id": shipment.shipment_id,
                    "cost_date": shipment_date.date(),
                    "cost_type": "TOLL",
                    "cost_amount": toll_charge,
                    "currency": "USD",
                    "transaction_type": "CHARGE",
                    "created_timestamp": (
                        shipment_date
                        + pd.Timedelta(
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                        )
                    ),
                }
            )

            cost_index += 1

        # Small proportion of shipments receive a correction or credit.
        if random.random() < 0.015:
            credit_amount = round(
                -base_freight
                * random.uniform(0.02, 0.15),
                2,
            )

            cost_records.append(
                {
                    "transportation_cost_id": (
                        f"CST-{cost_index:08d}"
                    ),
                    "shipment_id": shipment.shipment_id,
                    "cost_date": shipment_date.date(),
                    "cost_type": "CORRECTION",
                    "cost_amount": credit_amount,
                    "currency": "USD",
                    "transaction_type": "CREDIT",
                    "created_timestamp": (
                        shipment_date
                        + pd.Timedelta(
                            days=random.randint(1, 10),
                            hours=random.randint(0, 23),
                        )
                    ),
                }
            )

            cost_index += 1

    return pd.DataFrame(cost_records)


def generate_transportation_budgets(
    regions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate monthly transportation budgets by region.

    Grain:
    one row per month + region.
    """

    month_starts = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="MS",
    )

    base_monthly_budget = {
        "REG-001": 1_250_000,
        "REG-002": 950_000,
        "REG-003": 475_000,
    }

    budgets = []
    budget_index = 1

    for month in month_starts:
        month_number = month.month

        # Mild seasonal planning pattern.
        if month_number in {11, 12}:
            seasonal_multiplier = 1.12
        elif month_number in {6, 7, 8}:
            seasonal_multiplier = 1.06
        elif month_number in {1, 2}:
            seasonal_multiplier = 0.94
        else:
            seasonal_multiplier = 1.00

        for region in regions.itertuples(index=False):
            baseline = base_monthly_budget[
                region.region_id
            ]

            planning_variation = random.uniform(
                0.97,
                1.03,
            )

            budget_amount = round(
                baseline
                * seasonal_multiplier
                * planning_variation,
                2,
            )

            budgets.append(
                {
                    "budget_id": (
                        f"BUD-{budget_index:06d}"
                    ),
                    "budget_month": month.date(),
                    "region_id": region.region_id,
                    "budget_amount": budget_amount,
                    "currency": "USD",
                    "created_timestamp": (
                        month
                        - pd.Timedelta(days=30)
                        + pd.Timedelta(
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                        )
                    ),
                }
            )

            budget_index += 1

    return pd.DataFrame(budgets)


def generate_asset_movements(
    assets: pd.DataFrame,
    shipments: pd.DataFrame,
    locations: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate historical asset movement events.

    Grain:
    one row per asset movement or asset status event.

    The generator creates a realistic event history using:
    - asset lifecycle
    - shipment-related movements
    - repositioning
    - returns
    - maintenance transfers
    - status changes
    """

    active_locations = locations[
        locations["active_flag"]
    ].copy()

    location_ids = active_locations[
        "location_id"
    ].tolist()

    delivered_shipments = shipments[
        shipments["shipment_status"] == "DELIVERED"
    ].copy()

    delivered_shipments = delivered_shipments[
        delivered_shipments["actual_delivery_date"].notna()
    ]

    shipment_records = list(
        delivered_shipments.itertuples(index=False)
    )

    movement_records = []
    movement_index = 1

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)

    movement_types = [
        "SHIPMENT",
        "RETURN",
        "REPOSITION",
        "MAINTENANCE_TRANSFER",
        "STATUS_CHANGE",
    ]

    for asset in assets.itertuples(index=False):
        asset_created_date = pd.Timestamp(
            asset.created_date
        )

        effective_start_date = max(
            start_date,
            asset_created_date,
        )

        if pd.notna(asset.retirement_date):
            effective_end_date = min(
                end_date,
                pd.Timestamp(
                    asset.retirement_date
                ),
            )
        else:
            effective_end_date = end_date

        if effective_start_date > effective_end_date:
            continue

        current_location_id = asset.home_location_id
        current_status = "AVAILABLE"

        movement_count = random.randint(
            25,
            80,
        )

        event_dates = sorted(
            effective_start_date
            + pd.to_timedelta(
                np.random.randint(
                    0,
                    max(
                        1,
                        (
                            effective_end_date
                            - effective_start_date
                        ).days
                        + 1,
                    ),
                    size=movement_count,
                ),
                unit="D",
            )
        )

        for movement_date in event_dates:
            movement_type = random.choices(
                movement_types,
                weights=[
                    0.48,  # SHIPMENT
                    0.16,  # RETURN
                    0.20,  # REPOSITION
                    0.08,  # MAINTENANCE_TRANSFER
                    0.08,  # STATUS_CHANGE
                ],
                k=1,
            )[0]

            previous_status = current_status
            origin_location_id = current_location_id
            destination_location_id = None
            related_shipment_id = None

            if (
                movement_type == "SHIPMENT"
                and shipment_records
            ):
                shipment = random.choice(
                    shipment_records
                )

                origin_location_id = (
                    shipment.origin_location_id
                )

                destination_location_id = (
                    shipment.destination_location_id
                )

                related_shipment_id = (
                    shipment.shipment_id
                )

                current_location_id = (
                    destination_location_id
                )

                current_status = "IN_TRANSIT"

                # Completed shipment event leaves
                # the asset available at destination.
                new_status = "AVAILABLE"

            elif movement_type == "RETURN":
                destination_location_id = (
                    asset.home_location_id
                )

                current_location_id = (
                    destination_location_id
                )

                new_status = "AVAILABLE"

            elif movement_type == "REPOSITION":
                candidate_locations = [
                    location_id
                    for location_id in location_ids
                    if location_id
                    != current_location_id
                ]

                destination_location_id = (
                    random.choice(
                        candidate_locations
                    )
                )

                current_location_id = (
                    destination_location_id
                )

                new_status = "AVAILABLE"

            elif (
                movement_type
                == "MAINTENANCE_TRANSFER"
            ):
                candidate_locations = [
                    location_id
                    for location_id in location_ids
                    if location_id
                    != current_location_id
                ]

                destination_location_id = (
                    random.choice(
                        candidate_locations
                    )
                )

                current_location_id = (
                    destination_location_id
                )

                new_status = "MAINTENANCE"

            else:
                possible_statuses = [
                    "AVAILABLE",
                    "IN_USE",
                    "IN_TRANSIT",
                    "MAINTENANCE",
                ]

                new_status = random.choice(
                    possible_statuses
                )

                destination_location_id = (
                    current_location_id
                )

            movement_timestamp = (
                pd.Timestamp(movement_date)
                + pd.Timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                    seconds=random.randint(0, 59),
                )
            )

            movement_records.append(
                {
                    "asset_movement_id": (
                        f"MOV-{movement_index:09d}"
                    ),
                    "asset_id": asset.asset_id,
                    "movement_timestamp": (
                        movement_timestamp
                    ),
                    "origin_location_id": (
                        origin_location_id
                    ),
                    "destination_location_id": (
                        destination_location_id
                    ),
                    "movement_type": (
                        movement_type
                    ),
                    "previous_status": (
                        previous_status
                    ),
                    "new_status": new_status,
                    "related_shipment_id": (
                        related_shipment_id
                    ),
                }
            )

            current_status = new_status
            movement_index += 1

    return pd.DataFrame(
        movement_records
    )


def generate_operational_exceptions(
    shipments: pd.DataFrame,
    transportation_costs: pd.DataFrame,
    asset_movements: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate operational exceptions derived from shipment, cost,
    and asset movement behavior.

    Grain:
    one row per operational exception event.
    """

    exceptions = []
    exception_index = 1

    # ---------------------------------------------------------
    # Late delivery exceptions
    # ---------------------------------------------------------

    delivered_shipments = shipments[
        shipments["shipment_status"] == "DELIVERED"
    ].copy()

    delivered_shipments["actual_delivery_date"] = pd.to_datetime(
        delivered_shipments["actual_delivery_date"]
    )

    delivered_shipments["expected_delivery_date"] = pd.to_datetime(
        delivered_shipments["expected_delivery_date"]
    )

    late_shipments = delivered_shipments[
        delivered_shipments["actual_delivery_date"]
        > delivered_shipments["expected_delivery_date"]
    ].copy()

    for shipment in late_shipments.itertuples(index=False):
        late_days = (
            shipment.actual_delivery_date
            - shipment.expected_delivery_date
        ).days

        if late_days >= 5:
            severity = "CRITICAL"
        elif late_days >= 3:
            severity = "HIGH"
        elif late_days >= 2:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        resolved_flag = random.random() < 0.90

        resolution_date = None

        if resolved_flag:
            resolution_date = (
                shipment.actual_delivery_date
                + pd.Timedelta(days=random.randint(0, 5))
            ).date()

        exceptions.append(
            {
                "exception_id": f"EXC-{exception_index:08d}",
                "exception_type": "LATE_DELIVERY",
                "exception_date": shipment.actual_delivery_date.date(),
                "severity": severity,
                "shipment_id": shipment.shipment_id,
                "asset_id": None,
                "customer_id": shipment.customer_id,
                "carrier_id": shipment.carrier_id,
                "route_id": shipment.route_id,
                "location_id": shipment.destination_location_id,
                "description": (
                    f"Shipment delivered {late_days} day(s) late."
                ),
                "resolved_flag": resolved_flag,
                "resolution_date": resolution_date,
            }
        )

        exception_index += 1

    # ---------------------------------------------------------
    # Cancelled shipment exceptions
    # ---------------------------------------------------------

    cancelled_shipments = shipments[
        shipments["shipment_status"] == "CANCELLED"
    ]

    for shipment in cancelled_shipments.itertuples(index=False):
        exception_date = pd.Timestamp(
            shipment.shipment_date
        ).date()

        severity = random.choices(
            [
                "LOW",
                "MEDIUM",
                "HIGH",
            ],
            weights=[
                0.25,
                0.55,
                0.20,
            ],
            k=1,
        )[0]

        resolved_flag = random.random() < 0.95

        resolution_date = None

        if resolved_flag:
            resolution_date = (
                pd.Timestamp(exception_date)
                + pd.Timedelta(
                    days=random.randint(1, 7)
                )
            ).date()

        exceptions.append(
            {
                "exception_id": f"EXC-{exception_index:08d}",
                "exception_type": "CANCELLED_SHIPMENT",
                "exception_date": exception_date,
                "severity": severity,
                "shipment_id": shipment.shipment_id,
                "asset_id": None,
                "customer_id": shipment.customer_id,
                "carrier_id": shipment.carrier_id,
                "route_id": shipment.route_id,
                "location_id": shipment.origin_location_id,
                "description": "Shipment was cancelled.",
                "resolved_flag": resolved_flag,
                "resolution_date": resolution_date,
            }
        )

        exception_index += 1

    # ---------------------------------------------------------
    # Cost anomaly exceptions
    # ---------------------------------------------------------

    shipment_costs = (
        transportation_costs
        .groupby(
            "shipment_id",
            as_index=False,
        )["cost_amount"]
        .sum()
        .rename(
            columns={
                "cost_amount": "total_transportation_cost",
            }
        )
    )

    cost_threshold = shipment_costs[
        "total_transportation_cost"
    ].quantile(0.995)

    anomalous_costs = shipment_costs[
        shipment_costs["total_transportation_cost"]
        >= cost_threshold
    ]

    shipment_lookup = (
        shipments
        .set_index("shipment_id")
        .to_dict("index")
    )

    for cost_record in anomalous_costs.itertuples(index=False):
        shipment = shipment_lookup[
            cost_record.shipment_id
        ]

        exception_date = pd.Timestamp(
            shipment["shipment_date"]
        ).date()

        resolved_flag = random.random() < 0.80

        resolution_date = None

        if resolved_flag:
            resolution_date = (
                pd.Timestamp(exception_date)
                + pd.Timedelta(
                    days=random.randint(1, 10)
                )
            ).date()

        exceptions.append(
            {
                "exception_id": f"EXC-{exception_index:08d}",
                "exception_type": "COST_ANOMALY",
                "exception_date": exception_date,
                "severity": "HIGH",
                "shipment_id": cost_record.shipment_id,
                "asset_id": None,
                "customer_id": shipment["customer_id"],
                "carrier_id": shipment["carrier_id"],
                "route_id": shipment["route_id"],
                "location_id": shipment[
                    "destination_location_id"
                ],
                "description": (
                    "Shipment transportation cost exceeded "
                    "the high-cost anomaly threshold."
                ),
                "resolved_flag": resolved_flag,
                "resolution_date": resolution_date,
            }
        )

        exception_index += 1

    # ---------------------------------------------------------
    # Asset-related exceptions
    # ---------------------------------------------------------

    movement_sample = asset_movements.sample(
        frac=0.015,
        random_state=RANDOM_SEED,
    )

    for movement in movement_sample.itertuples(index=False):
        exception_type = random.choice(
            [
                "MISSING_ASSET",
                "DAMAGED_ASSET",
                "ROUTE_EXCEPTION",
            ]
        )

        severity = random.choices(
            [
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL",
            ],
            weights=[
                0.20,
                0.45,
                0.28,
                0.07,
            ],
            k=1,
        )[0]

        resolved_flag = random.random() < 0.82

        exception_date = pd.Timestamp(
            movement.movement_timestamp
        ).date()

        resolution_date = None

        if resolved_flag:
            resolution_date = (
                pd.Timestamp(exception_date)
                + pd.Timedelta(
                    days=random.randint(1, 14)
                )
            ).date()

        exceptions.append(
            {
                "exception_id": f"EXC-{exception_index:08d}",
                "exception_type": exception_type,
                "exception_date": exception_date,
                "severity": severity,
                "shipment_id": (
                    movement.related_shipment_id
                    if pd.notna(
                        movement.related_shipment_id
                    )
                    else None
                ),
                "asset_id": movement.asset_id,
                "customer_id": None,
                "carrier_id": None,
                "route_id": None,
                "location_id": (
                    movement.destination_location_id
                    if pd.notna(
                        movement.destination_location_id
                    )
                    else movement.origin_location_id
                ),
                "description": (
                    f"{exception_type.replace('_', ' ').title()} "
                    "detected during asset movement."
                ),
                "resolved_flag": resolved_flag,
                "resolution_date": resolution_date,
            }
        )

        exception_index += 1

    return pd.DataFrame(exceptions)


def inject_data_quality_defects(
    shipments: pd.DataFrame,
    transportation_costs: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """
    Create source-like copies of selected datasets containing
    controlled and reproducible data-quality defects.

    The clean datasets are preserved.

    Returns:
        shipments_raw
        transportation_costs_raw
        data_quality_issues
    """

    shipments_raw = shipments.copy()
    transportation_costs_raw = (
        transportation_costs.copy()
    )

    quality_issues = []
    issue_index = 1

    # ---------------------------------------------------------
    # Duplicate shipment records
    # ---------------------------------------------------------

    duplicate_count = max(
        1,
        round(
            len(shipments_raw)
            * DUPLICATE_SHIPMENT_RATE
        ),
    )

    duplicate_rows = shipments_raw.sample(
        n=duplicate_count,
        random_state=RANDOM_SEED + 1,
    ).copy()

    shipments_raw = pd.concat(
        [
            shipments_raw,
            duplicate_rows,
        ],
        ignore_index=True,
    )

    for shipment_id in duplicate_rows[
        "shipment_id"
    ]:
        quality_issues.append(
            {
                "issue_id": (
                    f"DQ-{issue_index:07d}"
                ),
                "dataset_name": "shipments",
                "record_key": shipment_id,
                "issue_type": (
                    "DUPLICATE_SHIPMENT"
                ),
                "field_name": (
                    "shipment_id"
                ),
                "expected_condition": (
                    "Shipment ID must be unique."
                ),
            }
        )

        issue_index += 1

    # ---------------------------------------------------------
    # Missing carrier references
    # ---------------------------------------------------------

    missing_carrier_count = max(
        1,
        round(
            len(shipments)
            * MISSING_CARRIER_RATE
        ),
    )

    missing_carrier_indices = (
        shipments_raw[
            shipments_raw[
                "carrier_id"
            ].notna()
        ]
        .sample(
            n=missing_carrier_count,
            random_state=RANDOM_SEED + 2,
        )
        .index
    )

    for row_index in missing_carrier_indices:
        shipment_id = shipments_raw.at[
            row_index,
            "shipment_id",
        ]

        shipments_raw.at[
            row_index,
            "carrier_id",
        ] = None

        quality_issues.append(
            {
                "issue_id": (
                    f"DQ-{issue_index:07d}"
                ),
                "dataset_name": "shipments",
                "record_key": shipment_id,
                "issue_type": (
                    "MISSING_CARRIER"
                ),
                "field_name": "carrier_id",
                "expected_condition": (
                    "Transportation shipments "
                    "should reference a valid carrier."
                ),
            }
        )

        issue_index += 1

    # ---------------------------------------------------------
    # Invalid delivery dates
    # ---------------------------------------------------------

    delivered_candidates = shipments_raw[
        (
            shipments_raw[
                "shipment_status"
            ]
            == "DELIVERED"
        )
        & shipments_raw[
            "shipment_date"
        ].notna()
        & shipments_raw[
            "actual_delivery_date"
        ].notna()
    ]

    invalid_date_count = max(
        1,
        round(
            len(shipments)
            * INVALID_DATE_RATE
        ),
    )

    invalid_date_indices = (
        delivered_candidates.sample(
            n=min(
                invalid_date_count,
                len(
                    delivered_candidates
                ),
            ),
            random_state=RANDOM_SEED + 3,
        )
        .index
    )

    for row_index in invalid_date_indices:
        shipment_id = shipments_raw.at[
            row_index,
            "shipment_id",
        ]

        shipment_date = pd.Timestamp(
            shipments_raw.at[
                row_index,
                "shipment_date",
            ]
        )

        shipments_raw.at[
            row_index,
            "actual_delivery_date",
        ] = (
            shipment_date
            - pd.Timedelta(
                days=random.randint(1, 5)
            )
        ).date()

        quality_issues.append(
            {
                "issue_id": (
                    f"DQ-{issue_index:07d}"
                ),
                "dataset_name": "shipments",
                "record_key": shipment_id,
                "issue_type": (
                    "INVALID_DELIVERY_DATE"
                ),
                "field_name": (
                    "actual_delivery_date"
                ),
                "expected_condition": (
                    "Actual delivery date "
                    "must not precede shipment date."
                ),
            }
        )

        issue_index += 1

    # ---------------------------------------------------------
    # Invalid shipment quantities
    # ---------------------------------------------------------

    valid_quantity_candidates = (
        shipments_raw[
            shipments_raw[
                "shipment_quantity"
            ] > 0
        ]
    )

    invalid_quantity_count = max(
        1,
        round(
            len(shipments)
            * INVALID_QUANTITY_RATE
        ),
    )

    invalid_quantity_indices = (
        valid_quantity_candidates.sample(
            n=min(
                invalid_quantity_count,
                len(
                    valid_quantity_candidates
                ),
            ),
            random_state=RANDOM_SEED + 4,
        )
        .index
    )

    for counter, row_index in enumerate(
        invalid_quantity_indices
    ):
        shipment_id = shipments_raw.at[
            row_index,
            "shipment_id",
        ]

        invalid_value = (
            0
            if counter % 2 == 0
            else -random.randint(1, 25)
        )

        shipments_raw.at[
            row_index,
            "shipment_quantity",
        ] = invalid_value

        quality_issues.append(
            {
                "issue_id": (
                    f"DQ-{issue_index:07d}"
                ),
                "dataset_name": "shipments",
                "record_key": shipment_id,
                "issue_type": (
                    "INVALID_SHIPMENT_QUANTITY"
                ),
                "field_name": (
                    "shipment_quantity"
                ),
                "expected_condition": (
                    "Shipment quantity must "
                    "be greater than zero."
                ),
            }
        )

        issue_index += 1

    # ---------------------------------------------------------
    # Extreme transportation cost anomalies
    # ---------------------------------------------------------

    positive_cost_candidates = (
        transportation_costs_raw[
            transportation_costs_raw[
                "cost_amount"
            ] > 0
        ]
    )

    cost_anomaly_count = max(
        1,
        round(
            len(
                transportation_costs_raw
            )
            * COST_ANOMALY_RATE
        ),
    )

    anomaly_indices = (
        positive_cost_candidates.sample(
            n=min(
                cost_anomaly_count,
                len(
                    positive_cost_candidates
                ),
            ),
            random_state=RANDOM_SEED + 5,
        )
        .index
    )

    for row_index in anomaly_indices:
        cost_id = (
            transportation_costs_raw.at[
                row_index,
                "transportation_cost_id",
            ]
        )

        original_amount = float(
            transportation_costs_raw.at[
                row_index,
                "cost_amount",
            ]
        )

        transportation_costs_raw.at[
            row_index,
            "cost_amount",
        ] = round(
            original_amount
            * random.uniform(
                8.0,
                20.0,
            ),
            2,
        )

        quality_issues.append(
            {
                "issue_id": (
                    f"DQ-{issue_index:07d}"
                ),
                "dataset_name": (
                    "transportation_costs"
                ),
                "record_key": cost_id,
                "issue_type": (
                    "EXTREME_COST_ANOMALY"
                ),
                "field_name": "cost_amount",
                "expected_condition": (
                    "Transportation cost "
                    "should fall within "
                    "reasonable business ranges."
                ),
            }
        )

        issue_index += 1

    return (
        shipments_raw,
        transportation_costs_raw,
        pd.DataFrame(
            quality_issues
        ),
    )


def main() -> None:
    faker = initialize_random_state()
    ensure_output_directories()

    print("OpsIntel BI synthetic data generator")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Output directory: {GENERATED_DATA_DIR}")
    print()

    regions = generate_regions()
    write_dataset(regions, "regions.csv")

    locations = generate_locations(faker, regions)
    write_dataset(locations, "locations.csv")

    customers = generate_customers(
        faker,
        regions,
        CUSTOMER_COUNT,
    )
    write_dataset(customers, "customers.csv")

    carriers = generate_carriers(
        faker,
        regions,
        CARRIER_COUNT,
    )
    write_dataset(carriers, "carriers.csv")

    routes = generate_routes(
        locations,
        ROUTE_COUNT,
    )
    write_dataset(routes, "routes.csv")

    assets = generate_assets(
        faker,
        locations,
        ASSET_COUNT,
    )
    write_dataset(assets, "assets.csv")
    
    shipments = generate_shipments(
        faker,
        customers,
        carriers,
        routes,
        locations,
        SHIPMENT_COUNT,
    )
    write_dataset(shipments, "shipments.csv")

    transportation_costs = generate_transportation_costs(
        shipments,
        carriers,
        routes,
    )
    write_dataset(
        transportation_costs,
        "transportation_costs.csv",
    )

    transportation_budgets = generate_transportation_budgets(
        regions,
    )
    write_dataset(
        transportation_budgets,
        "transportation_budgets.csv",
    )

    asset_movements = generate_asset_movements(
        assets,
        shipments,
        locations,
    )
    write_dataset(
        asset_movements,
        "asset_movements.csv",
    )

    operational_exceptions = (
    generate_operational_exceptions(
        shipments,
        transportation_costs,
        asset_movements,
    )
    )
    write_dataset(
        operational_exceptions,
        "operational_exceptions.csv",
    )

    (
    shipments_raw,
    transportation_costs_raw,
    data_quality_issues,
    ) = inject_data_quality_defects(
        shipments,
        transportation_costs,
    )

    write_dataset(
        shipments_raw,
        "shipments.csv",
        RAW_DATA_DIR,
    )

    write_dataset(
        transportation_costs_raw,
        "transportation_costs.csv",
        RAW_DATA_DIR,
    )

    write_dataset(
        data_quality_issues,
        "data_quality_issues.csv",
    )


if __name__ == "__main__":
    main()