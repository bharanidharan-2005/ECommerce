import os
import re

views_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace order creation to also update subscriber
old_create = '''        order = serializer.save(user=request.user, **extra)'''
new_create = '''        order = serializer.save(user=request.user, **extra)

        # Mark welcome coupon as used
        if extra.get("promo_code") and extra["promo_code"].code.upper() == "WELCOME10":
            from apps.accounts.models import NewsletterSubscriber
            sub = NewsletterSubscriber.objects.filter(email=request.user.email).first()
            if sub:
                sub.coupon_used = True
                sub.save(update_fields=['coupon_used'])'''

content = content.replace(old_create, new_create)
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("CheckoutView patched to update coupon_used")