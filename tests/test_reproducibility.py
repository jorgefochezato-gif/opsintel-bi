import hashlib
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
RAW_DIR = PROJECT_ROOT / "data" / "raw"

GENERATOR = (
    PROJECT_ROOT
    / "scripts"
    / "data_generation"
    / "generate.py"
)


def calculate_file_hash(
    file_path: Path,
) -> str:
    """
    Calculate the SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(8192),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def collect_dataset_hashes() -> dict[str, str]:
    """
    Collect hashes for every generated and raw CSV dataset.
    """
    hashes = {}

    for directory_name, directory in [
        ("generated", GENERATED_DIR),
        ("raw", RAW_DIR),
    ]:
        for file_path in sorted(
            directory.glob("*.csv")
        ):
            key = (
                f"{directory_name}/"
                f"{file_path.name}"
            )

            hashes[key] = calculate_file_hash(
                file_path
            )

    return hashes


def run_generator() -> None:
    """
    Execute the synthetic data generator using the
    same Python interpreter running the test suite.
    """
    result = subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        "Synthetic data generator failed.\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )


def test_generator_is_reproducible() -> None:
    """
    Running the generator repeatedly with the same
    configuration and random seed must produce
    byte-for-byte identical CSV files.
    """

    run_generator()

    first_run_hashes = (
        collect_dataset_hashes()
    )

    assert first_run_hashes, (
        "No generated CSV datasets were found."
    )

    run_generator()

    second_run_hashes = (
        collect_dataset_hashes()
    )

    assert (
        first_run_hashes
        == second_run_hashes
    ), (
        "Synthetic datasets changed between "
        "identical generator runs."
    )