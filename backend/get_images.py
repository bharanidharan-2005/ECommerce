import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.products.models import Product

products = Product.objects.filter(name__icontains="Mechanical")
for p in products:
    print(f"Product: {p.name}, Image: {p.image.name}")
