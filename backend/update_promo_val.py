import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            # Newsletter specific check
            if promo.code.upper() == "WELCOME10":
                subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
                if not subscriber:
                    return Response({"detail": "This offer is available for first-time customers only."}, status=status.HTTP_400_BAD_REQUEST)
                if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                    return Response({"detail": "Your welcome discount has expired."}, status=status.HTTP_400_BAD_REQUEST)
                if subscriber.coupon_used:
                    return Response({"detail": "This coupon has already been used."}, status=status.HTTP_400_BAD_REQUEST)"""

new_block = """            # Newsletter specific check
            subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
            if subscriber and promo.code.upper() == subscriber.welcome_coupon.upper():
                if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                    return Response({"detail": "Your welcome discount has expired."}, status=status.HTTP_400_BAD_REQUEST)
                if subscriber.coupon_used:
                    return Response({"detail": "This coupon has already been used."}, status=status.HTTP_400_BAD_REQUEST)
            elif promo.code.endswith("10") and "WELCOME" not in promo.code:
                # If it looks like a welcome coupon but isn't theirs
                if not subscriber or promo.code.upper() != subscriber.welcome_coupon.upper():
                    # We might want to allow it if it's just a generic coupon, but for username10:
                    pass"""

content = content.replace(old_block, new_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated PromoValidateView")
