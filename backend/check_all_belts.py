import os
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

belts = Product.objects.filter(name__icontains="Belt")
for belt in belts:
    print(f"Product: {belt.name}, Image: {belt.image}")
