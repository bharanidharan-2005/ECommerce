import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from apps.products.serializers import ProductSerializer

names = ["Vintage Aviator Sunglasses", "Cotton Crewneck T-Shirt", "Slim Fit Chino Pants", "Canvas Tote Bag"]
for n in names:
    p = Product.objects.get(name=n)
    s = ProductSerializer(p)
    print(f"Product {n}: Image Output: {s.data.get('image')}")
