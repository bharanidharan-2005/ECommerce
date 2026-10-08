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
    "Bluetooth Tracker Tag": "https://tse4.mm.bing.net/th/id/OIP.pfNjRJMacCBXZo8lVkVQGgHaHE?r=0&pid=Api&h=220&P=0",
    "gaming mouse": "https://tse4.mm.bing.net/th/id/OIP.EWOCp9rP53CaaGcDfU5WgAHaHa?r=0&pid=Api&h=220&P=0",
    "Classic Denim Jacket": "https://tse2.mm.bing.net/th/id/OIP.9aWW8pcEZv1nvSarnMYAjAHaHa?r=0&pid=Api&h=220&P=0",
    "Vintage Aviator Sunglasses": "https://tse1.mm.bing.net/th/id/OIP.TsJoK7vxQTbb7PZvVWmeowHaFj?r=0&pid=Api&h=220&P=0",
    "Cotton Crewneck T-Shirt": "https://tse3.mm.bing.net/th/id/OIP.nzUa-Tl40esiAFNTTVFn0gHaK8?r=0&pid=Api&h=220&P=0",
    "slimfit chino pants": "https://tse4.mm.bing.net/th/id/OIP.9kqyu2O3DWVu_CStPD38EQHaLW?r=0&pid=Api&h=220&P=0",
    "Canvas Tote Bag": "https://tse1.mm.bing.net/th/id/OIP.uSz54Nqz0RI3kx6OEXFzkAHaHX?r=0&pid=Api&h=220&P=0"
}

for name, url in items.items():
    try:
        try:
            p = Product.objects.get(name__iexact=name)
        except Product.DoesNotExist:
            print(f"Product {name} not found")
            continue
            
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        res.raise_for_status()
        
        jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(res.content)
            
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print(f"Successfully updated {name}")
    except Exception as e:
        print(f"Failed to update {name}: {e}")

