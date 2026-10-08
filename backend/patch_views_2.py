import os
import re

views_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = r'order = serializer.save\(user=request.user, \*\*extra\)'
new_code = '''order = serializer.save(user=request.user, **extra)

        # Mark coupon as used if WELCOME10
        if extra.get("promo_code") and extra["promo_code"].code.upper() == "WELCOME10":
            from apps.accounts.models import NewsletterSubscriber
            subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
            if subscriber:
                subscriber.coupon_used = True
                subscriber.save(update_fields=["coupon_used"])'''

content = content.replace(old_code, new_code)
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 2 applied to views.py")