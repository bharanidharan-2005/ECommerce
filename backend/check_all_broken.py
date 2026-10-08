import os
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

products = Product.objects.all()
for p in products:
    if "Belt" in p.name or "Knife" in p.name or "French Press" in p.name or "Diffuser" in p.name or "Wristwatch" in p.name or "Pencil" in p.name:
        print(f"{p.name}: {p.image.name}")
