from django.db import models


class Listing(models.Model):
    source_id = models.CharField(
        unique=True,
        max_length=256,
        help_text="External ID to avoid duplicates (e.g. BienIci ID)",
    )

    department_code = models.CharField(max_length=3, db_index=True)
    postal_code = models.CharField(max_length=10, db_index=True)
    city = models.CharField(max_length=128, db_index=True)

    annual_condominium_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.city} {self.postal_code} ({self.department_code}) - fees={self.annual_condominium_fees}"
