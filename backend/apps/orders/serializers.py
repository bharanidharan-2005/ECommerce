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

    promo_code_str = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    promo_code = serializers.StringRelatedField(read_only=True)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items",
            "full_name", "email", "address_line_1", "address_line_2",
            "city", "state", "postal_code", "country",
            "total_price", "item_count", "is_paid", "paid_at",
            "payment_method", "currency", "created_at", "promo_code_str", "promo_code", "discount_amount"
        )
        read_only_fields = ("id", "order_number", "total_price", "is_paid", "paid_at", "promo_code", "discount_amount")

    def create(self, validated_data):
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
                    raise serializers.ValidationError({"promo_code_str": "This offer is currently unavailable."})
                elif promo.valid_until and promo.valid_until < timezone.now():
                    raise serializers.ValidationError({"promo_code_str": "This coupon has expired."})
                else:
                    # Also check if it's their welcome coupon and if they already used it
                    from apps.accounts.models import NewsletterSubscriber
                    user = self.context['request'].user
                    if user and user.is_authenticated:
                        subscriber = NewsletterSubscriber.objects.filter(email=user.email).first()
                        if subscriber and promo.code.upper() == subscriber.welcome_coupon.upper():
                            if subscriber.coupon_used:
                                raise serializers.ValidationError({"promo_code_str": "This coupon has already been used."})
                            if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                                raise serializers.ValidationError({"promo_code_str": "Your welcome discount has expired."})
                    
                    promo_code_obj = promo
                    discount_amount = total * (promo.discount_percentage / 100)
            except PromoCode.DoesNotExist:
                raise serializers.ValidationError({"promo_code_str": "Invalid promo code."})
                
        # Apply discount
        total = total - discount_amount
        if total < 0:
            total = 0

        order = Order.objects.create(
            **validated_data, 
            total_price=total,
            promo_code=promo_code_obj,
            discount_amount=discount_amount
        )
        
        # Mark welcome coupon as used if applicable
        if promo_code_obj:
            user = self.context['request'].user
            if user and user.is_authenticated:
                from apps.accounts.models import NewsletterSubscriber
                subscriber = NewsletterSubscriber.objects.filter(email=user.email).first()
                if subscriber and promo_code_obj.code.upper() == subscriber.welcome_coupon.upper():
                    subscriber.coupon_used = True
                    subscriber.save(update_fields=['coupon_used'])
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
    promo_code = serializers.CharField(source='promo_code.code', read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "items", "total_price",
            "is_paid", "created_at", "full_name", "email",
            "address_line_1", "address_line_2", "city", "state",
            "postal_code", "country", "payment_method",
            "promo_code", "discount_amount"
        )

