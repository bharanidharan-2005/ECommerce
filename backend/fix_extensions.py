import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product

for product in Product.objects.all():
    slug = product.slug
    if os.path.exists(f'media/products/{slug}.jpg'):
        product.image.name = f'products/{slug}.jpg'
        product.save()
        print(f"Set {slug} to .jpg")
    elif os.path.exists(f'media/products/{slug}.png'):
        product.image.name = f'products/{slug}.png'
        product.save()
        print(f"Set {slug} to .png")
    else:
        print(f"Missing image for {slug}")
