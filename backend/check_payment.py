import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.orders.models import Order

order = Order.objects.order_by("-created_at").first()
if order:
    print(f"Order: {order.order_number}")
    print(f"Payment Method: '{order.payment_method}'")
    print(f"Shipping Address: '{order.address_line_1}', '{order.city}', '{order.country}'")
else:
    print("No orders found")
