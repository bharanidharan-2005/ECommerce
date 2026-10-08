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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 1. Mechanical Pencil Set (SSL ignore)
url_pencil = "https://cdn.quick-backup.shop/cdn/1529/2025/01/06/thumb100-main-Nicpro-2-PCS-09-mm-Metal-Mechanical-Pencils-Set-Drafting-Pencil-for-Artist-Writing-Sketching-Drawing-with-4-Tubes-HB-Lead-Refill-ampamp-Erasers-Eraser-7388901-4735836.jpg"
try:
    p = Product.objects.get(name="Mechanical Pencil Set")
    res = requests.get(url_pencil, headers=HEADERS, timeout=10, verify=False)
    if res.status_code == 200:
        jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(res.content)
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print("Updated Mechanical Pencil Set")
except Exception as e:
    print(f"Error pencil: {e}")

# 2. Portable SSD 1TB (use a free unsplash placeholder for an SSD or a reliable direct link)
url_ssd = "https://images.unsplash.com/photo-1600085816301-4081c7e937d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
try:
    p = Product.objects.get(name="Portable SSD 1TB")
    res = requests.get(url_ssd, headers=HEADERS, timeout=10)
    if res.status_code == 200:
        jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(res.content)
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print("Updated Portable SSD 1TB")
except Exception as e:
    print(f"Error SSD: {e}")

