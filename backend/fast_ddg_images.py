import os
import django
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from duckduckgo_search import DDGS

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

def update_product_ddg(p):
    slug = p.slug
    try:
        results = DDGS().images(f"high quality product photo {p.name}", max_results=3)
        if not results:
            print(f"No results for {p.name}")
            return
            
        jpg_path = os.path.join(products_dir, f"{slug}.jpg")
        
        # Try downloading up to 3 results until one works
        for res in results:
            img_url = res['image']
            try:
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response, open(jpg_path, 'wb') as out_file:
                    out_file.write(response.read())
                p.image.name = f"products/{slug}.jpg"
                p.save()
                print(f"Updated {p.name} with DDG image")
                return # success
            except Exception:
                continue # try next image
        print(f"All downloads failed for {p.name}")
    except Exception as e:
        print(f"Search failed for {p.name}: {e}")

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(update_product_ddg, products)

print("Done overwriting ALL images with exact matching DDG images!")
