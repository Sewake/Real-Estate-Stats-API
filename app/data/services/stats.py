from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from data.models import Listing
from django.db import models
from django.db.models import Aggregate, Avg, Count


@dataclass(frozen=True, slots=True)
class ChargesStats:
    count: int
    mean: Decimal
    q10: Decimal
    q90: Decimal


class Percentile(Aggregate):
    """
    PostgreSQL ordered-set aggregate:
    percentile_cont(p) WITHIN GROUP (ORDER BY expr)
    """

    function = "percentile_cont"
    template = "%(function)s(%(percentile_placeholder)s) WITHIN GROUP (ORDER BY %(expressions)s)"
    output_field = models.DecimalField(max_digits=14, decimal_places=6)

    def __init__(self, expression, percentile: float, **extra):
        self.percentile = float(percentile)
        super().__init__(expression, **extra)

    def as_sql(self, compiler, connection, **extra_context):
        # We inject the percentile as a SQL parameter (%s)
        extra_context["percentile_placeholder"] = "%s"
        sql, params = super().as_sql(compiler, connection, **extra_context)
        return sql, [self.percentile, *params]


def compute_charges_stats(
    department_code: str = None, city: str = None, postal_code: str = None
) -> ChargesStats:
    qs = Listing.objects.exclude(annual_condominium_fees__isnull=True)

    if department_code:
        qs = qs.filter(department_code=department_code)
    elif city:
        qs = qs.filter(city__iexact=city)
    elif postal_code:
        qs = qs.filter(postal_code=postal_code)

    agg = qs.aggregate(
        count=Count("id"),
        mean=Avg("annual_condominium_fees"),
        q10=Percentile("annual_condominium_fees", 0.10),
        q90=Percentile("annual_condominium_fees", 0.90),
    )

    if not agg["count"]:
        z = Decimal("0")
        return ChargesStats(count=0, mean=z, q10=z, q90=z)

    return ChargesStats(
        count=int(agg["count"]),
        mean=agg["mean"] or Decimal("0"),
        q10=agg["q10"] or Decimal("0"),
        q90=agg["q90"] or Decimal("0"),
    )
