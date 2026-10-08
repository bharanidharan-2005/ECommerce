import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product

keywords = ['sunglass', 'chino', 't-shirt', 'tote']
for p in Product.objects.all():
    for k in keywords:
        if k in p.name.lower():
            print(f"DB NAME: '{p.name}'")
