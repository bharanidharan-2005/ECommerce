from rest_framework import serializers

from apps.products.models import Product

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        # Client sends only product_id + quantity; name/price/subtotal are
        # derived server-side inside OrderSerializer.create() to prevent
        # price tampering.
        fields = ("id", "product_id", "product_name", "price", "quantity", "subtotal", "image")
        read_only_fields = ("id", "product_name", "price", "subtotal", "image")

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items",
            "full_name", "email", "address_line_1", "address_line_2",
            "city", "state", "postal_code", "country",
            "total_price", "item_count", "is_paid", "paid_at",
            "payment_method", "currency", "created_at",
        )
        read_only_fields = ("id", "order_number", "total_price", "is_paid", "paid_at")

    def create(self, validated_data):
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
        )
        for product, quantity, price in order_items:
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=price,
                quantity=quantity,
                image=product.image,
            )
            product.stock -= quantity
            product.save(update_fields=["stock"])
        return order


class MyOrderSerializer(serializers.ModelSerializer):
    """Order list serializer for the user's own history (read-only)."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items", "total_price",
            "is_paid", "created_at", "full_name", "email",
            "address_line_1", "address_line_2", "city", "state",
            "postal_code", "country", "payment_method",
        )
