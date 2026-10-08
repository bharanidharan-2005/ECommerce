from django.db import models


class ExchangeRate(models.Model):
    """Live/cached exchange rates against base currency USD."""

    currency_code = models.CharField(max_length=3, unique=True, db_index=True)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    symbol = models.CharField(max_length=5, default="$")
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("currency_code",)

    def __str__(self):
        return f"{self.currency_code}: {self.symbol} {self.rate}"


# Predefined currency symbols and names
CURRENCY_CHOICES = [
    ("USD", "$", "US Dollar"),
    ("EUR", "€", "Euro"),
    ("GBP", "£", "British Pound"),
    ("INR", "₹", "Indian Rupee"),
    ("CAD", "$", "Canadian Dollar"),
    ("AUD", "$", "Australian Dollar"),
    ("JPY", "¥", "Japanese Yen"),
    ("CNY", "¥", "Chinese Yuan"),
]


def ensure_default_rates():
    """Ensure default exchange rates exist in the database."""
    from django.db.models import Max
    from decimal import Decimal

    created = False
    for code, symbol, name in CURRENCY_CHOICES:
        obj, created_flag = ExchangeRate.objects.get_or_create(
            currency_code=code,
            defaults={"rate": Decimal("1.000000"), "symbol": symbol, "name": name},
        )
        if created_flag:
            created = True
    return created