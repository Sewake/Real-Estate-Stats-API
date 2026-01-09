from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_stats_filter_by_department_code(client, listings):
    resp = client.get("/api/stats/charges/", {"department_code": "33"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 6

    mean = Decimal(data["mean"]).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    assert mean == Decimal("1283.33")


@pytest.mark.django_db
def test_stats_filter_by_city_bordeaux(client, listings):
    resp = client.get("/api/stats/charges/", {"city": "Bordeaux"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 2
    assert Decimal(data["mean"]) == Decimal("1350")


@pytest.mark.django_db
def test_stats_filter_by_city_case_insensitive(client, listings):
    resp = client.get("/api/stats/charges/", {"city": "mÉrIgNaC"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 2
    assert Decimal(data["mean"]) == Decimal("1500")


@pytest.mark.django_db
def test_stats_filter_by_postal_code_33400(client, listings):
    resp = client.get("/api/stats/charges/", {"postal_code": "33400"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 2
    assert Decimal(data["mean"]) == Decimal("1000")


@pytest.mark.django_db
def test_stats_filter_by_postal_code_33000(client, listings):
    resp = client.get("/api/stats/charges/", {"postal_code": "33000"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 1
    assert Decimal(data["mean"]) == Decimal("1200")


@pytest.mark.django_db
def test_stats_filter_no_results_returns_zeros(client, listings):
    resp = client.get("/api/stats/charges/", {"postal_code": "99999"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["count"] == 0
    assert Decimal(data["mean"]) == Decimal("0")
    assert Decimal(data["q10"]) == Decimal("0")
    assert Decimal(data["q90"]) == Decimal("0")


@pytest.mark.django_db
def test_stats_requires_at_least_one_filter(client):
    resp = client.get("/api/stats/charges/")
    assert resp.status_code == 400
