from data.views import charges_form
from django.urls import path

urlpatterns = [
    path("stats/charges/", charges_form, name="charges-form"),
]
