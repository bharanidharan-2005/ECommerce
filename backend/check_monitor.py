import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product

for p in Product.objects.all():
    if 'monitor' in p.name.lower():
        print(p.name)
