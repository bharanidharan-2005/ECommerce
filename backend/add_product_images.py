"""One-off helper: downloads keyword-matched photos into media/products/
and attaches them to the seeded products."""
import os
import time
import urllib.request

from apps.products.models import Product

KEYWORDS = {
    "wireless-headphones-pro": "headphones",
    "smart-watch-ultra": "smartwatch",
    "mechanical-keyboard-rgb": "mechanical-keyboard",
    "classic-denim-jacket": "denim-jacket",
    "running-shoes-flex": "running-shoes",
    "yoga-mat-premium": "yoga",
    "ceramic-dinner-set-16pc": "tableware",
    "scented-candle-trio": "candles",
}

os.makedirs("media/products", exist_ok=True)

for product in Product.objects.all():
    keyword = KEYWORDS.get(product.slug, product.slug.split("-")[0])
    filename = f"products/{product.slug}.jpg"
    filepath = f"media/{filename}"
    url = f"https://loremflickr.com/800/800/{keyword}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(filepath, "wb") as out:
            out.write(resp.read())
        if os.path.getsize(filepath) < 5000:
            raise ValueError("downloaded file too small")
        product.image.name = filename
        product.save(update_fields=["image"])
        print(f"OK   {product.slug} <- {keyword}")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL {product.slug}: {exc}")
    time.sleep(1)
