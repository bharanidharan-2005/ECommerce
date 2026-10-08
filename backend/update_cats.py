import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category
fashion = Category.objects.filter(name='Fashion').first()
if fashion:
    fashion.name = 'Clothing'
    fashion.save()

home = Category.objects.filter(name='Home').first()
if home:
    home.name = 'Home & Garden'
    home.save()

for c in Category.objects.all():
    print(c.id, c.name)