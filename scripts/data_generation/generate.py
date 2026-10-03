import random

import numpy as np
import pandas as pd
from faker import Faker

from config import (
    GENERATED_DATA_DIR,
    LOCATION_COUNT,
    RANDOM_SEED,
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


def write_dataset(df: pd.DataFrame, filename: str) -> None:
    """
    Write a generated dataset to the configured output directory.
    """
    output_path = GENERATED_DATA_DIR / filename
    df.to_csv(output_path, index=False)

    print(f"Wrote {len(df):,} rows -> {output_path}")


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


if __name__ == "__main__":
    main()