from __future__ import annotations

from decimal import Decimal

import pytest
from data.models import Listing


@pytest.fixture
def dataset():
    return [
        # Bordeaux (33000 / 33100)
        dict(
            source_id="dataset:bordeaux-1",
            department_code="33",
            postal_code="33000",
            city="Bordeaux",
            annual_condominium_fees=Decimal("1200"),
        ),
        dict(
            source_id="dataset:bordeaux-2",
            department_code="33",
            postal_code="33100",
            city="Bordeaux",
            annual_condominium_fees=Decimal("1500"),
        ),
        # Talence (33400)
        dict(
            source_id="dataset:talence-1",
            department_code="33",
            postal_code="33400",
            city="Talence",
            annual_condominium_fees=Decimal("900"),
        ),
        dict(
            source_id="dataset:talence-2",
            department_code="33",
            postal_code="33400",
            city="Talence",
            annual_condominium_fees=Decimal("1100"),
        ),
        # Mérignac (33700)
        dict(
            source_id="dataset:merignac-1",
            department_code="33",
            postal_code="33700",
            city="Mérignac",
            annual_condominium_fees=Decimal("1300"),
        ),
        dict(
            source_id="dataset:merignac-2",
            department_code="33",
            postal_code="33700",
            city="Mérignac",
            annual_condominium_fees=Decimal("1700"),
        ),
    ]


@pytest.fixture
def listings(db, dataset):
    """
    Insert chef dataset into the database.
    """
    Listing.objects.bulk_create(
        [Listing(**row) for row in dataset],
        ignore_conflicts=True,
    )
    return dataset
