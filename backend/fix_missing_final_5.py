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
    "Wireless Headphones Pro": "https://tse3.mm.bing.net/th/id/OIP.xSenSj31eFSi-2lCI19ONQHaEK?r=0&pid=Api&h=220&P=0",
    "Smart Watch Ultra": "https://tse3.mm.bing.net/th/id/OIP.gYeoFLnqm0PCmcUe15jDFwHaHa?r=0&pid=Api&h=220&P=0",
    "Mechanical Keyboard RGB": "https://tse3.mm.bing.net/th/id/OIP.RqMILuEHekwDU6X_R1MejQHaE6?r=0&pid=Api&h=220&P=0",
    "Wireless Gaming Mouse": "https://tse2.mm.bing.net/th/id/OIP.31WOWdTI7ytFufkcZsxsaQHaHa?r=0&pid=Api&h=220&P=0",
    "USB-C Hub Adapter": "https://tse3.mm.bing.net/th/id/OIP.cTDaJHlYvdEfKsrDrKR3CgHaHa?r=0&pid=Api&h=220&P=0",
    "Noise-Canceling Earbuds": "https://tse3.mm.bing.net/th/id/OIP.gdLNv7otzKJD4f42k1tRKQHaIj?r=0&pid=Api&h=220&P=0",
    "Portable Power Bank 20000mAh": "https://tse4.mm.bing.net/th/id/OIP.yfzV7Pq40vFJNF0jLv7InwHaHj?r=0&pid=Api&h=220&P=0",
    "Smart Home Speaker": "https://tse1.mm.bing.net/th/id/OIP.LKd7CU2A_c-_B_IEfFYZuAHaFF?r=0&pid=Api&h=220&P=0",
    "Bluetooth Soundbar": "https://tse2.mm.bing.net/th/id/OIP.ErsNHmLnXtwXKZDbjTUQTwHaCa?r=0&pid=Api&h=220&P=0",
    "Soldering Iron Station": "https://tse1.mm.bing.net/th/id/OIP.rM7ti_1-mOdRscgGkCGL2AHaGv?r=0&pid=Api&h=220&P=0",
    "Ultra Wide Gaming Monitor": "https://tse3.mm.bing.net/th/id/OIP.HAnfXsUDeCGPmoZ8GkTdaQHaHa?r=0&pid=Api&h=220&P=0",
    "Portable SSD 1TB": "https://tse2.mm.bing.net/th/id/OIP.9fsqqlGF4E3cx6pap8oMWQHaFS?r=0&pid=Api&h=220&P=0"
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

