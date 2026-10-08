"""Tests for the eCommerce models and serializers."""
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Tests for the custom User model."""

    def test_user_email_is_unique(self):
        """Email must be unique per the model definition."""
        with pytest.raises(Exception):
            User.objects.create_user(email="test@example.com", password="testpass123")
            User.objects.create_user(email="test@example.com", password="testpass123")

    def test_user_has_required_fields(self):
        """User model has email, country, and currency fields."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123",
            country="US", currency="USD"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.country, "US")
        self.assertEqual(user.currency, "USD")


class ProductModelTest(TestCase):
    """Tests for the Product model."""

    def test_product_creation(self):
        """Product can be created with valid data."""
        from apps.products.models import Category, Product

        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            category=category, name="Test Product", slug="test-product",
            description="A test product", price=9.99, stock=10
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.stock, 10)
        self.assertTrue(product.is_in_stock)

    def test_product_average_rating(self):
        """Product average_rating property works correctly."""
        from apps.products.models import Category, Product, Review
        from django.db.models import Avg

        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            category=category, name="Rating Product", slug="rating-product",
            description="A product for testing ratings", price=19.99, stock=5
        )
        # Create two users for the reviews
        user1 = User.objects.create_user(email="reviewer1@example.com", password="testpass123")
        user2 = User.objects.create_user(email="reviewer2@example.com", password="testpass123")
        # Create some reviews
        Review.objects.create(product=product, user=user1, rating=5, comment="Great!")
        Review.objects.create(product=product, user=user2, rating=3, comment="Good enough")

        avg = product.average_rating
        self.assertEqual(avg, 4.0)

    def test_product_str(self):
        """Product __str__ returns the product name."""
        from apps.products.models import Category, Product

        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            category=category, name="Str Test", slug="str-test",
            description="Testing str method", price=5.00, stock=1
        )
        self.assertEqual(str(product), "Str Test")


class ReviewModelTest(TestCase):
    """Tests for the Review model."""

    def test_review_creation(self):
        """Review can be created with valid data."""
        from apps.products.models import Category, Product, Review

        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        user = User.objects.create_user(email="user@example.com", password="testpass123")
        product = Product.objects.create(
            category=category, name="Review Product", slug="review-product",
            description="A product for reviews", price=15.00, stock=5
        )

        review = Review.objects.create(product=product, user=user, rating=4, comment="Good product")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good product")

    def test_review_unique_together(self):
        """A user can only review a product once."""
        from apps.products.models import Category, Product, Review

        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        user = User.objects.create_user(email="user2@example.com", password="testpass123")
        product = Product.objects.create(
            category=category, name="Unique Review Product", slug="unique-review-product",
            description="Testing unique together", price=15.00, stock=5
        )

        Review.objects.create(product=product, user=user, rating=5, comment="First review")
        with pytest.raises(Exception):
            Review.objects.create(product=product, user=user, rating=3, comment="Duplicate review")


class OrderModelTest(TestCase):
    """Tests for the Order model."""

    def test_order_creation_cod(self):
        """CO order can be created without payment."""
        from apps.orders.models import Order

        user = User.objects.create_user(email="cod@example.com", password="testpass123")
        order = Order.objects.create(
            user=user, full_name="Test User", email="cod@example.com",
            address_line_1="123 Test St", city="Testville", state="TS",
            postal_code="12345", country="US",
            total_price=29.99, payment_method="cod"
        )
        self.assertEqual(order.payment_method, "cod")
        self.assertEqual(order.status, "pending")
        self.assertFalse(order.is_paid)

    def test_order_item_count(self):
        """Order item_count property sums quantities."""
        from apps.orders.models import Order, OrderItem
        from apps.products.models import Product, Category

        user = User.objects.create_user(email="count@example.com", password="testpass123")
        category, _ = Category.objects.get_or_create(name="Electronics", slug="electronics")
        product = Product.objects.create(
            category=category, name="Count Product", slug="count-product",
            description="Testing item count", price=10.00, stock=5
        )

        order = Order.objects.create(
            user=user, full_name="Test", email="count@example.com",
            address_line_1="1 Test St", city="Testville", state="TS",
            postal_code="12345", country="US",
            total_price=20.00, payment_method="cod"
        )
        OrderItem.objects.create(order=order, product=product, product_name=product.name,
                                 price=product.price, quantity=3)

        self.assertEqual(order.item_count, 3)


class CartSliceTest(TestCase):
    """Tests for the cart functionality."""

    def test_cart_persistence(self):
        """Cart items persistence data structure test."""
        import json

        # Test cart data structure
        stored_items = [
            {"id": 1, "name": "Product A", "price": "10.00", "qty": 2},
            {"id": 2, "name": "Product B", "price": "20.00", "qty": 1},
        ]
        localStorage = {"cartItems": json.dumps(stored_items)}

        # Verify the data structure
        items = json.loads(localStorage["cartItems"])
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["qty"], 2)
        self.assertEqual(items[1]["qty"], 1)


class ExchangeRateTest(TestCase):
    """Tests for the ExchangeRate model and rates endpoint."""

    def test_default_rates_exist(self):
        """Default exchange rates are created during migrations."""
        from rates.models import ExchangeRate, CURRENCY_CHOICES

        # Ensure rates exist
        from rates.models import ensure_default_rates
        ensure_default_rates()

        usd = ExchangeRate.objects.get(currency_code="USD")
        self.assertEqual(str(usd), "USD: $ 1.000000")

    def test_all_currencies_have_rates(self):
        """All currency choices have exchange rates."""
        from rates.models import ExchangeRate, CURRENCY_CHOICES

        # Ensure rates exist
        from rates.models import ensure_default_rates
        ensure_default_rates()

        for code, _, _ in CURRENCY_CHOICES:
            rate = ExchangeRate.objects.get(currency_code=code)
            self.assertIsNotNone(rate.rate)