"""
Catalog loader — syncs backend/catalog.json into the database.

Matching is done by slugified product NAME (the JSON's numeric ids don't
correspond to database PKs):
  - existing product  -> price / description / category / image updated
  - new product       -> created with stock=25
Images are downloaded from the provided URL (placehold.co) and stored in
media/products/ so Django's ImageField keeps serving them like any upload.
"""
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

import json
import urllib.request
from PIL import Image
from io import BytesIO

from django.utils.text import slugify

from apps.products.models import Category, Product

os.makedirs("media/products", exist_ok=True)

with open("catalog.json", encoding="utf-8") as fh:
    catalog = json.load(fh)

# Cache categories once
cats = {c.name: c for c in Category.objects.all()}
for name in {item["category"] for item in catalog}:
    if name not in cats:
        cats[name] = Category.objects.create(name=name, slug=slugify(name))

created = updated = skipped_img = 0

for item in catalog:
    slug = slugify(item["name"])
    defaults = {
        "category": cats[item["category"]],
        "description": item["description"],
        "price": str(item["price"]),
        "stock": 25,
    }
    product, was_created = Product.objects.get_or_create(slug=slug, defaults={"name": item["name"], **defaults})

    if not was_created:
        # Sync editable fields on existing rows
        changed = []
        for field, value in defaults.items():
            if getattr(product, field) != value:
                setattr(product, field, value)
                changed.append(field)
        if changed:
            product.save(update_fields=changed + ["updated_at"])
            updated += 1
    else:
        created += 1

    # ---- Image: download once, reuse afterwards ----
    img_path = f"media/products/{slug}.png"
    url = item["image_url"]
    # Force PNG format (placehold.co default may be SVG, which Pillow rejects)
    if "?" in url:
        base, qs = url.split("?", 1)
        url = f"{base}.png?{qs}"
    else:
        url = f"{url}.png"

    needs_download = not os.path.exists(img_path) or os.path.getsize(img_path) < 1000
    if needs_download:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(img_path, "wb") as out:
                out.write(resp.read())
            # Validate downloaded image with PIL
            with Image.open(img_path) as im:
                im.verify()
        except Exception as exc:  # noqa: BLE001
            print(f"IMG FAIL {slug}: {exc}")
            # Remove invalid image file
            if os.path.exists(img_path):
                os.remove(img_path)
            continue
    else:
        skipped_img += 1

    if product.image.name != f"products/{slug}.png":
        product.image.name = f"products/{slug}.png"
        product.save(update_fields=["image"])

print(f"Done. created={created}, updated={updated}, images_cached={skipped_img}, total={Product.objects.count()}")
