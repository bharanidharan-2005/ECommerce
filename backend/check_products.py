import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product
existing = {p.slug: p for p in Product.objects.all()}
print('Existing products by slug:')
for s in sorted(existing.keys()):
    print(f'  {s}: {existing[s].name} (id={existing[s].id})')