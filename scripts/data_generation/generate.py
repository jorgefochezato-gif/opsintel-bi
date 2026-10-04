import random

import numpy as np
import pandas as pd
from faker import Faker
from math import asin, cos, radians, sin, sqrt

from config import (
    ASSET_COUNT,
    CARRIER_COUNT,
    CUSTOMER_COUNT,
    END_DATE,
    GENERATED_DATA_DIR,
    LOCATION_COUNT,
    RANDOM_SEED,
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


def ensure_output_directory() -> None:
    """
    Ensure the generated-data directory exists before writing files.
    """
    GENERATED_DATA_DIR.mkdir(parents=True, exist_ok=True)


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


def write_dataset(df: pd.DataFrame, filename: str) -> None:
    """
    Write a generated dataset to the configured output directory.
    """
    output_path = GENERATED_DATA_DIR / filename
    df.to_csv(output_path, index=False)

    print(f"Wrote {len(df):,} rows -> {output_path}")


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


def main() -> None:
    faker = initialize_random_state()
    ensure_output_directory()

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

if __name__ == "__main__":
    main()