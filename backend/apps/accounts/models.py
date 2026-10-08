from django.conf import settings as django_settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


def get_default_currency():
    return "USD"


def get_default_country():
    return "US"


class CustomUserManager(BaseUserManager):
    """Custom user manager that uses email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with email as the username field."""
        import django
        from django.contrib.auth.hashers import make_password

        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        extra_fields.setdefault("email", email)

        user = self.model(**extra_fields)
        user.password = make_password(password) if password else ""
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with email as the username field."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("username", email)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user extending Django's built-in user with profile fields."""

    email = models.EmailField("email address", unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    country = models.CharField(
        max_length=2, default=get_default_country, db_index=True
    )
    currency = models.CharField(
        max_length=3, default=get_default_currency, db_index=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["country"]),
            models.Index(fields=["currency"]),
        ]

    def __str__(self):
        return self.email

    objects = CustomUserManager()


class StoreSetting(models.Model):
    settings = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Store Settings"

    def __str__(self):
        return "Global Store Settings"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        if created or not obj.settings:
            obj.settings = {
                "storeName": "ShopVerse",
                "storeEmail": "contact@shopverse.com",
                "supportEmail": "support@shopverse.com",
                "phone": "+91 9876543210",
                "description": "Premium E-commerce Store",
                "storeStatus": "open",
                "closureMessage": "We are temporarily closed.",
                "currency": "INR",
                "country": "India",
                "timezone": "Asia/Kolkata",
                "language": "English",
                "dateFormat": "DD/MM/YYYY",
                "numberFormat": "Indian",
                "emailNotifications": True,
                "inAppNotifications": True,
                "legalBusinessName": "ShopVerse Technologies Pvt Ltd",
                "gstin": "22AAAAA0000A1Z5",
                "pan": "ABCDE1234F",
                "businessAddress": "123 Tech Park",
                "city": "Bangalore",
                "state": "Karnataka",
                "pinCode": "560001",
                "orderIdPrefix": "ORD",
                "autoCancelUnpaid": True,
                "cancelAfterHours": 24,
                "shippingEnabled": True,
                "flatRate": 50,
                "freeShippingThreshold": 500,
                "taxEnabled": True,
                "defaultTaxRate": 18,
                "pricesIncludeTax": False,
                "returnsEnabled": True,
                "returnWindowDays": 7,
            }
            obj.save()
        return obj

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    welcome_coupon = models.CharField(max_length=50, blank=True)
    coupon_used = models.BooleanField(default=False)
    coupon_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
