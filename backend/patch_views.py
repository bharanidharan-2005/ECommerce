import os

views_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'NewsletterSubscriber' not in content.split('from .models')[1].split('\n')[0]:
    content = content.replace('from .models import User', 'from .models import User, NewsletterSubscriber')
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("views patched")