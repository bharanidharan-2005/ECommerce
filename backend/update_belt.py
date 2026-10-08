import os
import shutil
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

img_src = r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\genuine_leather_belt_1791024740246.jpg"
media_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\media\products"
os.makedirs(media_dir, exist_ok=True)

dest = os.path.join(media_dir, "genuine_leather_belt_new.jpg")
shutil.copy(img_src, dest)

belt = Product.objects.filter(name__icontains="Genuine Leather Belt").first()
if belt:
    belt.image.name = "products/genuine_leather_belt_new.jpg"
    belt.save()
    print("Updated Genuine Leather Belt")
else:
    print("Genuine Leather Belt not found in database")
