import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = Product.objects.all()
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

for p in products:
    slug = p.slug
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    png_path = os.path.join(products_dir, f"{slug}.png")
    
    if os.path.exists(jpg_path):
        p.image = f"products/{slug}.jpg"
        p.save()
        print(f"Updated {slug} to .jpg")
    elif os.path.exists(png_path):
        p.image = f"products/{slug}.png"
        p.save()
        print(f"Updated {slug} to .png")
    else:
        print(f"Missing image for {slug}")
