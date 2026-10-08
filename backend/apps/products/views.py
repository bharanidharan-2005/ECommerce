from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.db.models import Avg
from rest_framework import permissions, viewsets

from .models import Category, Product, Review, Wishlist
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, WishlistSerializer



import django_filters

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    sale = django_filters.BooleanFilter(method='filter_sale')

    class Meta:
        model = Product
        fields = ['category']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
        
    def filter_sale(self, queryset, name, value):
        from django.db.models import F
        if value:
            return queryset.filter(original_price__isnull=False, original_price__gt=F('price'))
        return queryset

@method_decorator(cache_page(60 * 15), name='list')
class ProductViewSet(viewsets.ModelViewSet):
    """
    List / retrieve / create / update products.
    Supports: ?search=, ?category=<id>, ?ordering=price|-price|created_at
    """
    queryset = (
        Product.objects.select_related("category")
        .prefetch_related("reviews")
        .annotate(rating_avg=Avg("reviews__rating"))
    )
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ("name", "description")
    ordering_fields = ("price", "created_at", "rating_avg")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


@method_decorator(cache_page(60 * 15), name='list')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        from django.db import IntegrityError
        product = Product.objects.get(pk=self.kwargs["product_pk"])
        try:
            serializer.save(user=self.request.user, product=product)
        except IntegrityError:
            raise ValidationError({"non_field_errors": ["You have already reviewed this product."]})

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Promotion
from .serializers import PromotionSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_promotion(request):
    now = timezone.now()
    promo = Promotion.objects.filter(
        active=True,
        start_date__lte=now,
        end_date__gte=now
    ).order_by('-priority', '-start_date').first()
    
    if promo:
        serializer = PromotionSerializer(promo)
        return Response(serializer.data)
    return Response({"detail": "No active promotion found"}, status=404)
