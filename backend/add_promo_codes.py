import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.orders.models import PromoCode
PromoCode.objects.get_or_create(code="WELCOME10", defaults={"discount_percentage": 10.00})
PromoCode.objects.get_or_create(code="SAVE20", defaults={"discount_percentage": 20.00})
print("Added promo codes: WELCOME10, SAVE20")
