import os
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

belt = Product.objects.filter(name__icontains="Belt").first()
if belt:
    print(f"Product: {belt.name}")
    print(f"Image: {belt.image}")
else:
    print("Belt not found")
