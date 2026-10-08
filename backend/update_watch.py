import os
import sys

# force clear any conflicting env vars
if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

pencil = Product.objects.filter(name__icontains="Mechanical Pencil").first()
if pencil:
    pencil.image.name = "products/mechanical_pencil_set.jpg"
    pencil.save()
    print("Updated Pencil")

watch = Product.objects.filter(name__icontains="Wristwatch").first()
if watch:
    watch.image.name = "products/mechanical_wristwatch.jpg"
    watch.save()
    print("Updated Watch")
else:
    print("Watch not found")
