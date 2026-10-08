import os
import sys
import django

# Set up Django environment
sys.path.append(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend")
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()

from apps.products.models import Product

updates_table_3 = {
    "Ultra-Wide Gaming Monitor": 39999,
    "Smart Home Hub": 7999,
    "Drone with 4K Camera": 34999,
    "Wireless Charging Pad": 1999,
    "Smart Thermostat": 14999,
    "Portable SSD 1TB": 8499,
    "Podcast Microphone": 9999,
    "Bluetooth Tracker Tag": 2499,
    "E-Reader": 10999,
    "Gaming Mouse": 4499,
    "Tablet Stand": 1499,
    "Remote": 1299,
    "Classic Denim Jacket": 2999,
    "Minimalist Leather Wallet": 1499,
    "Vintage Aviator Sunglasses": 1999,
    "Cotton Crewneck T-Shirt": 899,
    "Slim Fit Chino Pants": 1799,
    "Ceramic Dinner Set 16pc": 4999,
    "Scented Candle Trio": 1299,
    "Smart LED Bulb RGB": 999,
    "Ergonomic Office Chair": 12999,
    "Woven Throw Blanket": 2499,
    "Bamboo Cutting Board": 1499,
    "Stainless Steel French Press": 2499,
    "Essential Oil Diffuser": 2999,
    "Memory Foam Pillow": 2499,
    "Minimalist Wall Clock": 1499,
    "Robot Vacuum Cleaner": 24999,
    "Indoor Potted Succulent Set": 1499,
    "Minimalist Desk Lamp": 2999,
    "Cast Iron Skillet": 2499,
    "French Press Coffee Maker": 1999,
    "Espresso Machine": 29999,
    "Linen Bed Sheets": 4999,
    "Aromatherapy Diffuser": 2499,
    "Chef's Knife": 4999,
    "Fleece Throw Blanket": 1499,
    "Ceramic Plant Pot": 999,
    "Satin Pillowcase Set": 999,
    "Running Shoes Flex": 5999,
    "Yoga Mat Premium": 1999,
    "Adjustable Dumbbell Set": 14999,
    "Resistance Band Kit": 1499,
    "Insulated Water Bottle 32oz": 1999,
}

for product in Product.objects.all():
    name = product.name
    if name in updates_table_3:
        product.price = updates_table_3[name]
        product.save()
        print(f"Updated {name} to {product.price}")

