import random

import numpy as np
import pandas as pd
from faker import Faker

from config import GENERATED_DATA_DIR, RANDOM_SEED


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

    The region list is intentionally deterministic and business-defined
    rather than randomly generated.
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
    print(f"Example deterministic company name: {faker.company()}")
    print()

    regions = generate_regions()
    write_dataset(regions, "regions.csv")


if __name__ == "__main__":
    main()