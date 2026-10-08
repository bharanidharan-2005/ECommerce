import os
import django
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

os.makedirs(products_dir, exist_ok=True)

def update_product_ai(p):
    slug = p.slug
    # Build a descriptive prompt for the AI image generator
    prompt = urllib.parse.quote(f"A high quality studio product photo of a {p.name}")
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=800&height=800&nologo=true"
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response, open(jpg_path, 'wb') as out_file:
            out_file.write(response.read())
        
        p.image.name = f"products/{slug}.jpg"
        p.save()
        print(f"Updated {p.name} with AI matching image")
    except Exception as e:
        print(f"Failed {p.name}: {e}")

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(update_product_ai, products)

print("Done overwriting ALL images with exact matching AI images!")
