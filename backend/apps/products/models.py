from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.files.base import ContentFile
import os
from io import BytesIO
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.PROTECT
    )
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["category", "-created_at"]),
        ]

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(models.Avg("rating"))
        return round(agg["rating__avg"] or 0, 1)

    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        # Image compression & WebP conversion
        if self.image and hasattr(self.image, 'file'):
            try:
                img = Image.open(self.image.file)
                # Ensure RGB mode for WebP conversion
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if > 1080x1080
                img.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='WEBP', quality=85)
                output.seek(0)
                
                filename = os.path.splitext(self.image.name)[0] + '.webp'
                self.image.save(filename, ContentFile(output.read()), save=False)
            except Exception as e:
                # Fallback to original if Pillow fails
                print(f"Image processing failed: {e}")
                pass
                
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} -> {self.product.name} ({self.rating})"

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="wishlist", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="wishlisted_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} -> {self.product.name}"

class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True)
    discount = models.CharField(max_length=50, blank=True)
    button_text = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='promotions', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-priority', '-start_date']

    def __str__(self):
        return self.title
