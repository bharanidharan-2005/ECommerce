import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\serializers.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price", "stock",
            "image", "category", "category_name", "average_rating",
            "reviews", "created_at",
        )'''

replacement = '''class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price", "original_price", "discount_percentage", "stock",
            "image", "category", "category_name", "average_rating",
            "reviews", "created_at",
        )

    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated serializers.py')
else:
    print('Could not find target in serializers.py')
