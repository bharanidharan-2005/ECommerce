import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\serializers.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_create = """    def create(self, validated_data):
        items_data = validated_data.pop("items")
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

        order = Order.objects.create(**validated_data, total_price=total)"""

new_create = """    def create(self, validated_data):
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
content = content.replace(old_create, new_create)

# Also update the fields in OrderSerializer to include promo code if needed? 
# Maybe just leave them out of Meta.fields since we inject it manually in the view.

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated OrderSerializer")
