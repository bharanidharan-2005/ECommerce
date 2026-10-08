import os
import sys
import django

# Set up Django environment
sys.path.append(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend")
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()

from apps.products.models import Product

updates_table_4 = {
    "High-Density Foam Roller": 2499,
    "Microfiber Gym Towel": 1999,
    "Jump Rope with Counter": 2999,
    "Hiking Backpack 40L": 9999,
    "Boxing Gloves 14oz": 6999,
    "Tennis Racket Pro": 14999,
    "Compression Knee Sleeve": 2999,
    "Stainless Steel Water Bottle": 3999,
    "Bicycle Helmet": 8999,
    "Hiking Backpack": 14999,
    "Resistance Band Set": 2999,
    "Tennis Racket": 19999,
    "Camping Tent": 24999,
    "Yoga Block Set": 2499,
    "Stand Up Paddleboard": 45999,
    "Jump Rope": 1999,
    "Foam Roller": 2999,
}

for product in Product.objects.all():
    name = product.name
    if name in updates_table_4:
        product.price = updates_table_4[name]
        product.save()
        print(f"Updated {name} to {product.price}")

