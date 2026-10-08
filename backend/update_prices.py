import os
import sys
import django

# Set up Django environment
sys.path.append(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend")
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()

from apps.products.models import Product

# Exact mapping from table 1
updates_table_1 = {
    "Waterproof Winter Coat": 2499,
    "Canvas Tote Bag": 699,
    "Suede Chelsea Boots": 2499,
    "Knitted Winter Beanie": 399,
    "Genuine Leather Belt": 799,
    "Canvas Weekend Duffel": 1499,
    "Cotton Crewneck Sweater": 1299,
    "Graphic T-Shirt": 599,
    "Leather Dress Shoes": 2499,
    "Winter Parka Coat": 2999,
    "Knitted Beanie": 399,
    "Leather Belt": 799,
    "Sneaker Cleaning Kit": 499,
    "Raspberry Pi 4 Model B": 10999,
    "37-in-1 Sensor Kit": 1439,
    "Soldering Iron Station": 1999,
    "Mechanical Switch Tester": 219,
    "4K Action Camera": 3999,
}

# The user explicitly asked to fix these too
updates_table_2 = {
    "Polarized Aviator Sunglasses": 1199,
    "Leather Wallet": 499,
    "Mechanical Pencil Set": 199,
    "Mechanical Wristwatch": 2499,
    "Gold Plated Necklace": 599,
    "Silver Hoop Earrings": 499,
    "Wireless Headphones Pro": 1999,
    "Smart Watch Ultra": 3499,
    "Mechanical Keyboard RGB": 1299,
    "4K Ultra-Wide Monitor": 4499,
    "Wireless Gaming Mouse": 599,
    "USB-C Hub Adapter": 349,
    "Noise-Canceling Earbuds": 1499,
    "Portable Power Bank 20000mAh": 499,
    "Smart Home Speaker": 899,
    "Web Camera 1080p": 699,
    "Bluetooth Soundbar": 1199,
    "ESP32 Development Board": 199,
}

def nice_round(val):
    if val < 500:
        return round(val / 10) * 10 - 1
    elif val < 2000:
        return round(val / 100) * 100 - 1
    else:
        return round(val / 500) * 500 - 1

for product in Product.objects.all():
    name = product.name
    if name in updates_table_1:
        product.price = updates_table_1[name]
        product.save()
        print(f"Updated {name} to {product.price}")
    elif name in updates_table_2:
        product.price = updates_table_2[name]
        product.save()
        print(f"Updated {name} to {product.price} (from table 2 estimates)")
    else:
        # Auto convert any other ones
        new_price = nice_round(float(product.price) * 96.10)
        product.price = new_price
        product.save()
        print(f"Updated {name} to {product.price} (auto-converted)")

