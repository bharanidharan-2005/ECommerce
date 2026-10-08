import os
import django
import shutil

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

files_to_copy = {
    "Vintage Aviator Sunglasses": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\vintage_aviator_sunglasses_1790606010711.jpg",
    "Cotton Crewneck T-Shirt": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\cotton_crewneck_tshirt_1790606046668.jpg",
    "Slim Fit Chino Pants": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\slim_fit_chino_pants_1790606083502.jpg",
    "Canvas Tote Bag": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\canvas_tote_bag_1790606113022.jpg",
    "Winter Parka Coat": r"C:\Users\M.BHARANIDHARAN\.gemini\antigravity-ide\brain\170ef81e-5f06-4bd9-8788-23e909024624\winter_parka_coat_1790606251968.jpg"
}

for name, src_path in files_to_copy.items():
    try:
        p = Product.objects.get(name__iexact=name)
        dst_path = os.path.join(products_dir, f"{p.slug}.jpg")
        
        # copy the generated image
        shutil.copy2(src_path, dst_path)
        
        # update DB
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print(f"Successfully updated {name} with high-res studio shot.")
    except Exception as e:
        print(f"Failed to update {name}: {e}")
