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
    Generate deterministic operational locations across the enterprise regions.
    """

    location_types = [
        "PLANT",
        "WAREHOUSE",
        "SERVICE_CENTER",
        "CUSTOMER_SITE",
        "PORT",
    ]

    country_catalog = {
        "REG-001": [
            ("United States", "US"),
            ("Canada", "CA"),
            ("Mexico", "MX"),
        ],
        "REG-002": [
            ("Germany", "DE"),
            ("Belgium", "BE"),
            ("France", "FR"),
            ("Spain", "ES"),
            ("Netherlands", "NL"),
        ],
        "REG-003": [
            ("Argentina", "AR"),
            ("Brazil", "BR"),
            ("Chile", "CL"),
            ("Colombia", "CO"),
            ("Peru", "PE"),
        ],
    }

    locations = []

    region_ids = regions["region_id"].tolist()

    for index in range(1, LOCATION_COUNT + 1):
        region_id = random.choice(region_ids)
        country_name, country_code = random.choice(country_catalog[region_id])

        location_type = random.choice(location_types)

        location_id = f"LOC-{index:04d}"

        city = faker.city()
        state_province = faker.state()

        latitude = round(random.uniform(-55.0, 60.0), 6)
        longitude = round(random.uniform(-130.0, 30.0), 6)

        active_flag = random.random() > 0.05

        locations.append(
            {
                "location_id": location_id,
                "location_name": f"{city} {location_type.replace('_', ' ').title()}",
                "location_type": location_type,
                "city": city,
                "state_province": state_province,
                "country": country_name,
                "country_code": country_code,
                "region_id": region_id,
                "latitude": latitude,
                "longitude": longitude,
                "active_flag": active_flag,
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