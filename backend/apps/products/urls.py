from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, ReviewViewSet, WishlistViewSet, active_promotion

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register('categories', CategoryViewSet, basename='category')
router.register('', ProductViewSet, basename='product')
router.register(r'(?P<product_pk>\d+)/reviews', ReviewViewSet, basename='review')

urlpatterns = [path('promotions/active/', active_promotion, name='active_promotion'), path('', include(router.urls))]
