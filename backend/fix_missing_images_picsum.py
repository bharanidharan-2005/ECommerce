import os
import django
import urllib.request

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = Product.objects.all()
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

os.makedirs(products_dir, exist_ok=True)

missing = []

for p in products:
    slug = p.slug
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    png_path = os.path.join(products_dir, f"{slug}.png")
    
    if os.path.exists(jpg_path):
        if p.image.name != f"products/{slug}.jpg":
            p.image.name = f"products/{slug}.jpg"
            p.save()
    elif os.path.exists(png_path):
        if p.image.name != f"products/{slug}.png":
            p.image.name = f"products/{slug}.png"
            p.save()
    else:
        missing.append(p)

import time

for p in missing:
    slug = p.slug
    url = f"https://picsum.photos/seed/{slug}/800/800"
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(jpg_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        
        p.image.name = f"products/{slug}.jpg"
        p.save()
        print(f"Downloaded and set image for {p.name}")
        time.sleep(0.5) 
    except Exception as e:
        print(f"Failed to download image for {p.name}: {e}")

print("Done fixing images with Picsum!")
