from data.api.views import ChargesStatsView
from django.urls import path

urlpatterns = [
    path("stats/charges/", ChargesStatsView.as_view(), name="charges-stats"),
]
