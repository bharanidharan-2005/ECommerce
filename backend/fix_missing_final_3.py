import os
import django
import requests

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
}

fallback_url = "https://loremflickr.com/800/800/candle"
name = "Scented Candle Trio"
try:
    p = Product.objects.get(name=name)
    print(f"Downloading {name} from fallback URL")
    res = requests.get(fallback_url, headers=HEADERS, timeout=10, verify=False)
    res.raise_for_status()
    
    jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
    with open(jpg_path, 'wb') as f:
        f.write(res.content)
        
    p.image.name = f"products/{p.slug}.jpg"
    p.save()
    print(f"Successfully updated {name}")
except Exception as e:
    print(f"Failed to download/update {name}: {e}")

