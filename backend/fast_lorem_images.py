import os
import django
import urllib.request
import urllib.parse
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

for p in products:
    slug = p.slug
    # Take the most descriptive word from the name to improve chances
    keyword = p.name.split()[-1]
    
    # Try different combinations if needed
    if len(p.name.split()) > 1:
        keyword = f"{p.name.split()[-2]},{p.name.split()[-1]}"
    
    url = f"https://loremflickr.com/800/800/{urllib.parse.quote(keyword)}/all"
    
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response, open(jpg_path, 'wb') as out_file:
            out_file.write(response.read())
        p.image.name = f"products/{slug}.jpg"
        p.save()
        print(f"Downloaded loremflickr image for {p.name} using keyword '{keyword}'")
    except Exception as e:
        print(f"Download failed for {p.name}: {e}")
    time.sleep(1) # be polite

print("Finished updating images via loremflickr!")
