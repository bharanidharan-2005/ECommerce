import os
import sys
import shutil
import django

# Set up Django environment
sys.path.append(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend")
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()

from apps.products.models import Product

media_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\media\products"
os.makedirs(media_dir, exist_ok=True)

updates = [
    {
        "name": "High-Density Foam Roller",
        "source": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\foam_roller_1791220760399.jpg",
        "filename": "foam_roller.jpg"
    },
    {
        "name": "Microfiber Gym Towel",
        "source": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\gym_towel_1791220775645.jpg",
        "filename": "gym_towel.jpg"
    },
    {
        "name": "Jump Rope with Counter",
        "source": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\jump_rope_1791220788315.jpg",
        "filename": "jump_rope.jpg"
    }
]

for item in updates:
    # copy the file
    dest = os.path.join(media_dir, item["filename"])
    shutil.copy2(item["source"], dest)
    
    # update database
    try:
        product = Product.objects.get(name=item["name"])
        product.image = f"products/{item['filename']}"
        product.save()
        print(f"Updated {item['name']} image to {product.image}")
    except Product.DoesNotExist:
        print(f"Product {item['name']} not found")

