import os
import re

views_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_validate = '''if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                    return Response({"detail": "Your welcome discount has expired."}, status=status.HTTP_400_BAD_REQUEST)'''
new_validate = '''if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                    return Response({"detail": "Your welcome discount has expired."}, status=status.HTTP_400_BAD_REQUEST)
                if subscriber.coupon_used:
                    return Response({"detail": "This coupon has already been used."}, status=status.HTTP_400_BAD_REQUEST)'''
content = content.replace(old_validate, new_validate)

old_checkout = '''if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                        raise ValueError("Your welcome discount has expired.")'''
new_checkout = '''if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                        raise ValueError("Your welcome discount has expired.")
                    if subscriber.coupon_used:
                        raise ValueError("This coupon has already been used.")'''
content = content.replace(old_checkout, new_checkout)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 3 applied to views.py")