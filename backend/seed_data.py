from apps.products.models import Category, Product, Review
from apps.accounts.models import User

categories = ["Electronics", "Fashion", "Home", "Sports"]
cats = {}
for name in categories:
    cat, _ = Category.objects.get_or_create(
        name=name,
        defaults={"slug": name.lower()},
    )
    cats[name] = cat

samples = [
    ("Wireless Headphones Pro", "Electronics", 199.99, "Premium noise-cancelling wireless headphones with 40h battery life."),
    ("Smart Watch Ultra", "Electronics", 349.00, "Fitness tracking, GPS, and always-on display."),
    ("Mechanical Keyboard RGB", "Electronics", 129.50, "Hot-swappable switches with per-key RGB lighting."),
    ("Classic Denim Jacket", "Fashion", 79.90, "Timeless denim jacket, unisex fit."),
    ("Running Shoes Flex", "Sports", 89.99, "Lightweight running shoes with responsive cushioning."),
    ("Yoga Mat Premium", "Sports", 39.99, "Non-slip 6mm eco-friendly yoga mat."),
    ("Ceramic Dinner Set 16pc", "Home", 119.00, "Elegant stoneware set for four."),
    ("Scented Candle Trio", "Home", 24.95, "Vanilla, sandalwood and ocean scents."),
]

admin = User.objects.filter(is_superuser=True).first()

for name, cat_name, price, desc in samples:
    product, created = Product.objects.get_or_create(
        slug=name.lower().replace(" ", "-"),
        defaults={
            "name": name,
            "category": cats[cat_name],
            "description": desc,
            "price": price,
            "stock": 25,
            "image": f"products/{name.lower().replace(' ', '-')}.jpg",
        },
    )
    if created and admin:
        Review.objects.create(product=product, user=admin, rating=5, comment="Excellent quality!")

print(f"Seeded {Product.objects.count()} products across {Category.objects.count()} categories.")
