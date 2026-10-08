from rest_framework import serializers

from .models import Category, Product, Review, Wishlist, Promotion

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "product", "user", "user_email", "rating", "comment", "created_at")
        read_only_fields = ("id", "user", "created_at", "product")

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price", "original_price", "discount_percentage", "stock",
            "image", "category", "category_name", "average_rating",
            "reviews", "created_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0

    def get_image(self, obj):
        if obj.image:
            img_str = str(obj.image)
            if img_str.startswith('data:image') or img_str.startswith('http'):
                return img_str
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image")

    def get_image(self, obj):
        if obj.image:
            img_str = str(obj.image)
            if img_str.startswith('data:image') or img_str.startswith('http'):
                return img_str
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Wishlist
        fields = ("id", "user", "product", "product_details", "created_at")
        read_only_fields = ("id", "user", "created_at", "product")

class PromotionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            img_str = str(obj.image)
            if img_str.startswith('data:image') or img_str.startswith('http'):
                return img_str
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

