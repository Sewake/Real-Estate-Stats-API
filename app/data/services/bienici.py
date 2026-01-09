from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

import requests

BIENICI_JSON_URL = "https://www.bienici.com/realEstateAd.json"


@dataclass(frozen=True, slots=True)
class BieniciAd:
    bienici_id: str
    city: str
    postal_code: str
    department_code: str
    annual_fees: Decimal | None


def extract_bienici_id(url: str) -> str:
    """
    Accepts:
    - https://www.bienici.com/annonce/.../<bienici_id>
    Returns: <bienici_id>
    """
    url = url.split("?q")[0]
    m = re.search(r"/annonce/[^?#]+/([^/?#]+)$", url.strip())
    if not m:
        raise ValueError("Invalid Bienici URL format")
    return m.group(1)


def fetch_bienici_ad(bienici_id: str, timeout_s: int = 10) -> dict[str, Any]:
    r = requests.get(BIENICI_JSON_URL, params={"id": bienici_id}, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def parse_bienici_ad(payload: dict[str, Any]) -> BieniciAd:
    bienici_id = payload["id"]
    city = payload.get("city") or ""
    postal_code = payload.get("postalCode") or ""
    department_code = payload.get("departmentCode") or ""

    fees_raw = payload.get("annualCondominiumFees")
    annual_fees = None
    if fees_raw is not None and str(fees_raw).strip() != "":
        annual_fees = Decimal(str(fees_raw))

    if not (city and postal_code and department_code):
        raise ValueError("Bienici payload missing required location fields")

    return BieniciAd(
        bienici_id=bienici_id,
        city=city,
        postal_code=postal_code,
        department_code=department_code,
        annual_fees=annual_fees,
    )
