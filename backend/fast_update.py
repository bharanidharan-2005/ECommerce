import os
import django
import urllib.request
from concurrent.futures import ThreadPoolExecutor

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

os.makedirs(products_dir, exist_ok=True)

def update_product(p):
    slug = p.slug
    url = f"https://picsum.photos/seed/{slug}/800/800"
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response, open(jpg_path, 'wb') as out_file:
            out_file.write(response.read())
        
        p.image.name = f"products/{slug}.jpg"
        p.save()
        print(f"Updated {p.name}")
    except Exception as e:
        print(f"Failed {p.name}: {e}")

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(update_product, products)

print("Done overwriting ALL images!")
