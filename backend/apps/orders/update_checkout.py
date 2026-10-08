import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_checkout = """        serializer = self.get_serializer(
            data={**request.data, "user": None}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        extra = {"payment_method": payment_method, "currency": currency}"""

new_checkout = """        serializer = self.get_serializer(
            data={**request.data, "user": None}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        extra = {"payment_method": payment_method, "currency": currency}
        
        # Process promo code
        promo_code_str = request.data.get("promo_code")
        if promo_code_str:
            from django.utils import timezone
            from decimal import Decimal
            try:
                promo = PromoCode.objects.get(code__iexact=promo_code_str, active=True)
                if promo.valid_from and promo.valid_from > timezone.now():
                    raise ValueError("Promo code not valid yet")
                if promo.valid_until and promo.valid_until < timezone.now():
                    raise ValueError("Promo code expired")
                
                # Calculate subtotal manually to apply discount
                subtotal = Decimal(0)
                from apps.products.models import Product
                for item in request.data.get("items", []):
                    prod = Product.objects.get(pk=item["product_id"])
                    subtotal += prod.price * int(item["quantity"])
                
                discount_amount = (subtotal * promo.discount_percentage) / Decimal(100)
                extra["promo_code"] = promo
                extra["discount_amount"] = discount_amount
            except Exception as e:
                return Response({"detail": f"Invalid promo code: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
"""
content = content.replace(old_checkout, new_checkout)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CheckoutView with promo logic")
