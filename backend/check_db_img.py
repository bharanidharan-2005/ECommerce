import os
import django
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product

names = ["Vintage Aviator Sunglasses", "Cotton Crewneck T-Shirt", "Slim Fit Chino Pants", "Canvas Tote Bag"]
for n in names:
    p = Product.objects.get(name=n)
    print(f"Product {n}: Image Field: {p.image.name} File path exists? {os.path.exists(p.image.path) if p.image else False}")

