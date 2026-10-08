import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\serializers.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add promo_code_str to fields
old_meta = """    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items",
            "full_name", "email", "address_line_1", "address_line_2",
            "city", "state", "postal_code", "country",
            "total_price", "item_count", "is_paid", "paid_at",
            "payment_method", "currency", "created_at",
        )"""
new_meta = """    promo_code_str = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items",
            "full_name", "email", "address_line_1", "address_line_2",
            "city", "state", "postal_code", "country",
            "total_price", "item_count", "is_paid", "paid_at",
            "payment_method", "currency", "created_at", "promo_code_str"
        )"""
content = content.replace(old_meta, new_meta)

# 2. Update create logic
old_create = """    def create(self, validated_data):
        items_data = validated_data.pop("items")
        
        # Extract promo fields if provided
        promo_code = validated_data.pop("promo_code", None)
        discount_amount = validated_data.pop("discount_amount", 0)

        total = 0
        order_items = []

        for item in items_data:
            product = Product.objects.select_for_update().get(pk=item["product_id"])
            quantity = item["quantity"]
            if product.stock < quantity:
                raise serializers.ValidationError(
                    {"detail": f"Insufficient stock for '{product.name}'."}
                )
            order_items.append((product, quantity, product.price))
            total += product.price * quantity
            
        # Apply discount
        total = total - discount_amount
        if total < 0:
            total = 0

        order = Order.objects.create(
            **validated_data, 
            total_price=total,
            promo_code=promo_code,
            discount_amount=discount_amount
        )"""

new_create = """    def create(self, validated_data):
        from apps.orders.models import PromoCode
        from django.utils import timezone
        
        items_data = validated_data.pop("items")
        promo_code_str = validated_data.pop("promo_code_str", None)
        
        total = 0
        order_items = []

        for item in items_data:
            product = Product.objects.select_for_update().get(pk=item["product_id"])
            quantity = item["quantity"]
            if product.stock < quantity:
                raise serializers.ValidationError(
                    {"detail": f"Insufficient stock for '{product.name}'."}
                )
            order_items.append((product, quantity, product.price))
            total += product.price * quantity
            
        discount_amount = 0
        promo_code_obj = None
        
        if promo_code_str:
            try:
                promo = PromoCode.objects.get(code__iexact=promo_code_str, active=True)
                if promo.valid_from and promo.valid_from > timezone.now():
                    pass
                elif promo.valid_until and promo.valid_until < timezone.now():
                    pass
                else:
                    promo_code_obj = promo
                    discount_amount = total * (promo.discount_percentage / 100)
            except PromoCode.DoesNotExist:
                pass
                
        # Apply discount
        total = total - discount_amount
        if total < 0:
            total = 0

        order = Order.objects.create(
            **validated_data, 
            total_price=total,
            promo_code=promo_code_obj,
            discount_amount=discount_amount
        )"""

content = content.replace(old_create, new_create)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated OrderSerializer")
