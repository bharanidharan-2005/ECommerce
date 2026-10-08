import os
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

updates = {
    "Genuine Leather Belt": "products/genuine_leather_belt_new.jpg",
    "Chef's Knife": "products/chefs_knife_new.jpg",
    "Stainless Steel French Press": "products/french_press_new.jpg",
    "Essential Oil Diffuser": "products/essential_oil_diffuser_new.jpg",
    "Mechanical Wristwatch": "products/mechanical_wristwatch.jpg",
    "Mechanical Pencil Set": "products/mechanical_pencil_set.jpg"
}

for name, img_path in updates.items():
    product = Product.objects.filter(name__iexact=name).first()
    if product:
        product.image.name = img_path
        product.save()
        print(f"Fixed: {name}")
    else:
        print(f"Not Found: {name}")
