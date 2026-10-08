import os
import django
import urllib.request
import urllib.parse
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

def fetch_wikimedia_image(query):
    # Try to find a related image on Wikimedia Commons
    url = f"https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url&format=json&gsrlimit=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ECommerce/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                imageinfo = page_info.get('imageinfo', [])
                if imageinfo:
                    return imageinfo[0].get('url')
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None

import time

for p in products:
    slug = p.slug
    img_url = fetch_wikimedia_image(p.name)
    if not img_url:
        # Fallback to a broader search
        words = p.name.split()
        if len(words) > 1:
            img_url = fetch_wikimedia_image(words[-1]) # e.g. "Wallet" instead of "Minimalist Leather Wallet"
            
    if img_url:
        print(f"Found image for {p.name}: {img_url}")
        jpg_path = os.path.join(products_dir, f"{slug}.jpg")
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0 ECommerce/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response, open(jpg_path, 'wb') as out_file:
                out_file.write(response.read())
            p.image.name = f"products/{slug}.jpg"
            p.save()
        except Exception as e:
            print(f"Download failed for {img_url}: {e}")
    else:
        print(f"No Wikimedia image for {p.name}")
    time.sleep(1) # Be polite

print("Finished Wikimedia update!")
