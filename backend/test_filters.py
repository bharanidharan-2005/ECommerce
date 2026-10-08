import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_config.settings')
django.setup()

from django.test import Client

c = Client()
res = c.get('/api/products/?min_price=10&in_stock=true')
print('Status:', res.status_code)
# print(res.json())
