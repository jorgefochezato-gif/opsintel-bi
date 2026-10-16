from pathlib import Path

import pandas as pd
import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"

DATABASE_URL = (
    "postgresql://opsintel:opsintel@localhost:5433/opsintel"
)


def query_dataframe(sql: str) -> pd.DataFrame:
    with psycopg.connect(DATABASE_URL) as connection:
        return pd.read_sql_query(
            sql,
            connection,
        )


def test_staging_shipment_row_count_matches_clean_reference() -> None:
    clean_shipments = pd.read_csv(
        GENERATED_DIR / "shipments.csv"
    )

    staging_count = query_dataframe(
        """
        SELECT COUNT(*) AS row_count
        FROM staging.shipments_clean;
        """
    )["row_count"].iloc[0]

    assert staging_count == len(clean_shipments)


def test_staging_shipment_ids_match_clean_reference() -> None:
    clean_shipments = pd.read_csv(
        GENERATED_DIR / "shipments.csv",
        usecols=["shipment_id"],
    )

    staging_shipments = query_dataframe(
        """
        SELECT shipment_id
        FROM staging.shipments_clean;
        """
    )

    clean_ids = set(
        clean_shipments["shipment_id"]
    )

    staging_ids = set(
        staging_shipments["shipment_id"]
    )

    assert staging_ids == clean_ids


def test_staging_cost_row_count_matches_raw_source() -> None:
    raw_costs = pd.read_csv(
        PROJECT_ROOT
        / "data"
        / "raw"
        / "transportation_costs.csv"
    )

    staging_count = query_dataframe(
        """
        SELECT COUNT(*) AS row_count
        FROM staging.transportation_costs_clean;
        """
    )["row_count"].iloc[0]

    assert staging_count == len(raw_costs)


def test_staging_has_no_duplicate_shipments() -> None:
    result = query_dataframe(
        """
        SELECT COUNT(*) AS duplicate_count
        FROM (
            SELECT shipment_id
            FROM staging.shipments_clean
            GROUP BY shipment_id
            HAVING COUNT(*) > 1
        ) duplicates;
        """
    )

    assert result["duplicate_count"].iloc[0] == 0


def test_staging_has_no_nonpositive_shipment_quantities() -> None:
    result = query_dataframe(
        """
        SELECT COUNT(*) AS invalid_count
        FROM staging.shipments_clean
        WHERE shipment_quantity <= 0;
        """
    )

    assert result["invalid_count"].iloc[0] == 0


def test_staging_has_no_impossible_delivery_dates() -> None:
    result = query_dataframe(
        """
        SELECT COUNT(*) AS invalid_count
        FROM staging.shipments_clean
        WHERE actual_delivery_date < shipment_date;
        """
    )

    assert result["invalid_count"].iloc[0] == 0


def test_missing_carriers_are_preserved_as_warnings() -> None:
    result = query_dataframe(
        """
        SELECT
            COUNT(*) AS warning_count
        FROM staging.shipments_clean
        WHERE carrier_id IS NULL
          AND quality_status = 'WARNING';
        """
    )

    assert result["warning_count"].iloc[0] > 0