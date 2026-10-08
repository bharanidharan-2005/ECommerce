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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

items = {
    "Woven Throw Blanket": "https://cerqular.com/cdn/shop/files/Graphite_CashmereThrow-1-1-437981.jpg?v=1758691384",
    "Ergonomic Office Chair": "https://images.openai.com/static-rsc-4/qe-Ojh-ObQtwE_srpat4VAdO8rpqpGqYYcNiG_j5fAJzxRDRNK80VnhjGkY41rmitaNpIjGu9equY6AL-NZkFhqdrJ6K5tac0LzgaqUbwCNeV2mXIGQHYfUpS4v2UgvKfP09SYxQt_DpPgB0G-Sbrh3mypTI02lTN5-NjPKWjU0bR1z5Zj7yNFBns2AArbp1?purpose=fullsize"
}

for name, url in items.items():
    try:
        p = Product.objects.get(name=name)
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        res.raise_for_status()
        
        jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(res.content)
            
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print(f"Successfully updated {name}")
    except Product.DoesNotExist:
        print(f"Product {name} not found")
    except Exception as e:
        print(f"Failed to update {name}: {e}")

