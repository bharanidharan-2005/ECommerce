import os
import django
import urllib.request
import time
import urllib.parse

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = Product.objects.all()
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')

os.makedirs(products_dir, exist_ok=True)

for p in products:
    slug = p.slug
    # url encode the product name
    prompt = urllib.parse.quote(p.name)
    url = f"https://image.pollinations.ai/prompt/high%20quality%20product%20photo%20of%20{prompt}?width=800&height=800&nologo=true"
    jpg_path = os.path.join(products_dir, f"{slug}.jpg")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(jpg_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        
        p.image.name = f"products/{slug}.jpg"
        p.save()
        print(f"Downloaded AI image for {p.name}")
        time.sleep(0.5) 
    except Exception as e:
        print(f"Failed to download image for {p.name}: {e}")

print("Done generating images!")
