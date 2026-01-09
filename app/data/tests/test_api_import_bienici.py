from __future__ import annotations

from decimal import Decimal

import pytest
import responses
from data.models import Listing
from data.services.bienici import BIENICI_JSON_URL
from rest_framework.test import APIClient


@pytest.mark.django_db
@responses.activate
def test_import_bienici_creates_listing():
    client = APIClient()

    bienici_id = "century-21-202_2907_27607"
    url = f"https://www.bienici.com/annonce/vente/paris-12e/appartement/3pieces/{bienici_id}"

    responses.add(
        method=responses.GET,
        url=BIENICI_JSON_URL,
        match=[responses.matchers.query_param_matcher({"id": bienici_id})],
        json={
            "id": bienici_id,
            "city": "Paris 12e",
            "postalCode": "75012",
            "departmentCode": "75",
            "annualCondominiumFees": 130,
        },
        status=200,
    )

    resp = client.post("/api/listings/import-bienici/", {"url": url}, format="json")
    assert resp.status_code == 201

    payload = resp.json()
    assert payload["created"] is True
    assert payload["source_id"] == bienici_id

    listing = Listing.objects.get(source_id=bienici_id)
    assert listing.city == "Paris 12e"
    assert listing.postal_code == "75012"
    assert listing.department_code == "75"
    assert listing.annual_condominium_fees == Decimal("130")


@pytest.mark.django_db
@responses.activate
def test_import_bienici_is_idempotent_updates_existing():
    client = APIClient()

    bienici_id = "ag941082-491612573"
    url = f"https://www.bienici.com/annonce/vente/vincennes/appartement/2pieces/{bienici_id}"

    # First response
    responses.add(
        responses.GET,
        BIENICI_JSON_URL,
        match=[responses.matchers.query_param_matcher({"id": bienici_id})],
        json={
            "id": bienici_id,
            "city": "Vincennes",
            "postalCode": "94300",
            "departmentCode": "94",
            "annualCondominiumFees": 1950,
        },
        status=200,
    )

    resp1 = client.post("/api/listings/import-bienici/", {"url": url}, format="json")
    assert resp1.status_code == 201

    # Second response: different fees (simulate update)
    responses.add(
        responses.GET,
        BIENICI_JSON_URL,
        match=[responses.matchers.query_param_matcher({"id": bienici_id})],
        json={
            "id": bienici_id,
            "city": "Vincennes",
            "postalCode": "94300",
            "departmentCode": "94",
            "annualCondominiumFees": 2100,
        },
        status=200,
    )

    resp2 = client.post("/api/listings/import-bienici/", {"url": url}, format="json")
    assert resp2.status_code == 200
    assert resp2.json()["created"] is False

    listing = Listing.objects.get(source_id=bienici_id)
    assert listing.annual_condominium_fees == Decimal("2100")
