import sys
from apps.products.models import Product
for p in Product.objects.all():
    print(p.name, p.image.name)
