from data.api.views import ChargesStatsView, ImportBieniciView
from django.urls import path

urlpatterns = [
    path("stats/charges/", ChargesStatsView.as_view(), name="charges-stats"),
    path(
        "listings/import-bienici/", ImportBieniciView.as_view(), name="import-bienici"
    ),
]
