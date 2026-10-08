import os
import re

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add PromoCode to imports
if "PromoCode" not in content:
    content = content.replace("from .models import Order, OrderItem", "from .models import Order, OrderItem, PromoCode")

# 2. Add PromoValidateView
promo_view = """
class PromoValidateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"detail": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        
        try:
            promo = PromoCode.objects.get(code__iexact=code, active=True)
            if promo.valid_from && promo.valid_from > timezone.now():
                return Response({"detail": "This code is not valid yet."}, status=status.HTTP_400_BAD_REQUEST)
            if promo.valid_until && promo.valid_until < timezone.now():
                return Response({"detail": "This code has expired."}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                "code": promo.code,
                "discount_percentage": float(promo.discount_percentage)
            })
        except PromoCode.DoesNotExist:
            return Response({"detail": "Invalid promo code."}, status=status.HTTP_400_BAD_REQUEST)

class CheckoutView(generics.CreateAPIView):
"""
# Replace valid_from && with valid_from and (did it inside string above? wait, Python uses `and`. Let me fix it before replacing)
promo_view = promo_view.replace("&&", "and")

if "PromoValidateView" not in content:
    content = content.replace("class CheckoutView(generics.CreateAPIView):", promo_view)

# 3. Update CheckoutView's logic to handle promo code and apply discount
# Need to find the part where `subtotal` is summed and `total_price` is set
# Let's see if we can do this via python regex

# This is tricky without seeing the whole file. Let's dump the whole file to check the logic first, or just insert it securely.
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Added PromoValidateView. Will check CheckoutView next.")
