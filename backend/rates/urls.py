from django.urls import path

from .views import exchange_rate_list


urlpatterns = [
    path("rates/", exchange_rate_list, name="exchange-rate-list"),
]