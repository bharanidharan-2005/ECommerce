import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\views.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """        expires_at = timezone.now() + timedelta(days=7)
        subscriber = NewsletterSubscriber.objects.create(
            email=email,
            welcome_coupon="WELCOME10",
            coupon_expires_at=expires_at
        )
            
        return Response({
            "message": "Successfully subscribed!",
            "coupon": "WELCOME10",
            "expires_at": expires_at.isoformat(),
            "discount_percentage": 10,
            "min_order": 999
        }, status=201)"""

new_block = """        expires_at = timezone.now() + timedelta(days=7)
        username = email.split('@')[0]
        username = ''.join(e for e in username if e.isalnum())
        if not username:
            username = "USER"
        coupon_code = f"{username}10".upper()
        
        from apps.orders.models import PromoCode
        promo, created = PromoCode.objects.get_or_create(
            code=coupon_code,
            defaults={'discount_percentage': 10, 'active': True}
        )

        subscriber = NewsletterSubscriber.objects.create(
            email=email,
            welcome_coupon=coupon_code,
            coupon_expires_at=expires_at
        )
            
        return Response({
            "message": "Successfully subscribed!",
            "coupon": coupon_code,
            "expires_at": expires_at.isoformat(),
            "discount_percentage": 10,
            "min_order": 999
        }, status=201)"""

content = content.replace(old_block, new_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated NewsletterSubscribeView")
