import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import PromoCode
from decimal import Decimal

promo, created = PromoCode.objects.get_or_create(code='WELCOME10', defaults={
    'discount_percentage': Decimal('10.00'),
    'min_order_amount': Decimal('999.00'),
    'max_discount_amount': Decimal('500.00'),
    'first_order_only': True
})
if not created:
    promo.discount_percentage = Decimal('10.00')
    promo.min_order_amount = Decimal('999.00')
    promo.max_discount_amount = Decimal('500.00')
    promo.first_order_only = True
    promo.save()
print('WELCOME10 coupon ensured.')