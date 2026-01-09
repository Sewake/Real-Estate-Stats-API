import csv
import logging
from decimal import Decimal
from pathlib import Path

from django.db import transaction

from .models import Listing

logger = logging.getLogger(__name__)


DATASET_DIR = Path(__file__).resolve().parent / "dataset"


def parse_decimal(value: str | None) -> Decimal | None:
    if not value:
        return None
    try:
        return Decimal(value)
    except Exception:
        return None


@transaction.atomic
def import_file(path: Path) -> int:
    """
    Import a single CSV file into Listing table.
    Returns number of imported rows.
    """
    POSTAL_CODE_MAX_CHARS = 5
    count = 0

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        listings = []

        for row in reader:
            source_id = row.get("AD_URLS") or ""
            if source_id:
                source_id = source_id.split("/")[-1]
            department_code = row.get("DEPT_CODE")
            postal_code = row.get("ZIP_CODE")
            city = row.get("CITY")

            fees = parse_decimal(row.get("CONDOMINIUM_EXPENSES"))

            # Skip invalid or absurd fees to avoid DB overflow
            if fees is None or fees < 0 or fees > 1_000_000:
                continue
            if not (source_id and department_code and postal_code and city):
                # Skip incomplete rows
                continue
            if len(postal_code) > POSTAL_CODE_MAX_CHARS:
                continue

            listings.append(
                Listing(
                    source_id=source_id,
                    department_code=str(department_code),
                    postal_code=str(postal_code),
                    city=str(city),
                    annual_condominium_fees=fees,
                )
            )

        Listing.objects.bulk_create(listings, batch_size=1000, ignore_conflicts=True)
        count = len(listings)
    logger.info(f"Imported {count} rows from {path.name}")
    return count


def import_all() -> None:
    csv_files = list(DATASET_DIR.glob("*.csv"))
    if not csv_files:
        raise RuntimeError(f"No CSV files found in {DATASET_DIR}")

    total = 0
    for csv_file in csv_files:
        count = import_file(csv_file)
        total += count

    logger.info(f"Total imported rows: {total}")
