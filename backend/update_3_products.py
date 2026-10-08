import os
import shutil
import sys

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.products.models import Product

media_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\media\products"
os.makedirs(media_dir, exist_ok=True)

updates = [
    {
        "name": "Chef's Knife",
        "src": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\chefs_knife_1791119029534.jpg",
        "dest": "chefs_knife_new.jpg"
    },
    {
        "name": "French Press",
        "src": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\french_press_1791119335082.jpg",
        "dest": "french_press_new.jpg"
    },
    {
        "name": "Diffuser",
        "src": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\essential_oil_diffuser_1791119365016.jpg",
        "dest": "essential_oil_diffuser_new.jpg"
    }
]

for update in updates:
    shutil.copy(update["src"], os.path.join(media_dir, update["dest"]))
    product = Product.objects.filter(name__icontains=update["name"]).first()
    if product:
        product.image.name = f"products/{update['dest']}"
        product.save()
        print(f"Updated {update['name']}")
    else:
        print(f"Failed to find {update['name']}")
