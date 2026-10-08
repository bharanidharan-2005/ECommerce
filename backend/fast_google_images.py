import os
import django
import requests
from bs4 import BeautifulSoup
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

products = list(Product.objects.all())
media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_google_image(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
    try:
        res = requests.get(search_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Google images are often in an 'img' tag inside specific classes, 
        # or embedded in scripts. A basic scraper might find the first actual img with a src starting with http
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and src.startswith('http') and 'gstatic' not in src:
                return src
                
        # Fallback if first method fails, gstatic is ok if it's the only one
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and src.startswith('http') and 'images/branding' not in src:
                return src
                
    except Exception as e:
        print(f"Error fetching Google Image for {query}: {e}")
    return None

for p in products:
    slug = p.slug
    img_url = get_google_image(p.name + " product photo")
    
    if img_url:
        jpg_path = os.path.join(products_dir, f"{slug}.jpg")
        try:
            res = requests.get(img_url, headers=HEADERS, timeout=10)
            with open(jpg_path, 'wb') as out_file:
                out_file.write(res.content)
            p.image.name = f"products/{slug}.jpg"
            p.save()
            print(f"Updated {p.name} via Google Images")
        except Exception as e:
            print(f"Download failed for {p.name}: {e}")
    else:
        print(f"No image found for {p.name}")
    
    time.sleep(1) # Polite delay

print("Finished updating images via Google Images!")
