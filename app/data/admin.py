from django.contrib import admin

from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source_id",
        "department_code",
        "postal_code",
        "city",
        "annual_condominium_fees",
    )
    list_filter = (
        "department_code",
        "postal_code",
        "city",
    )

    search_fields = (
        "source_id",
        "city",
        "postal_code",
        "department_code",
    )
    readonly_fields = ("created_at",)

    # Layout
    fieldsets = (
        (
            "Identifiers",
            {
                "fields": (
                    "id",
                    "source_id",
                ),
            },
        ),
        (
            "Location",
            {
                "fields": ("department_code", "postal_code", "city"),
            },
        ),
        (
            "Metrics",
            {
                "fields": ("annual_condominium_fees",),
            },
        ),
        (
            "Debug",
            {
                "fields": ("created_at",),
            },
        ),
    )
