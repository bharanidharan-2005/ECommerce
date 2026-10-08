import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

# Clear old deals
Product.objects.update(original_price=None)

# Select random 12 products
products = list(Product.objects.all())
random.shuffle(products)
deals = products[:12]

for p in deals:
    # 20% to 50% more expensive original price
    factor = random.uniform(1.2, 1.5)
    p.original_price = round(float(p.price) * factor, 2)
    p.save()

print(f'Seeded {len(deals)} deals.')
