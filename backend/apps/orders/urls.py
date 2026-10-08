from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CheckoutView,
    MyOrdersView,
    StripePublishableKeyView,
    StripeWebhookView,
    AdminOrderViewSet,
    AdminPromoCodeViewSet,
    AdminDashboardStatsView,
    AdminNotificationsView,
    CancelOrderView,
    PromoValidateView,
)

router = DefaultRouter()
router.register(r"admin", AdminOrderViewSet, basename="admin-orders")
router.register(r"admin-promos", AdminPromoCodeViewSet, basename="admin-promos")

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("promo/validate/", PromoValidateView.as_view(), name="promo_validate"),
    path("my/", MyOrdersView.as_view(), name="my_orders"),
    path("<int:pk>/cancel/", CancelOrderView.as_view(), name="cancel_order"),
    path("stripe/publishable-key/", StripePublishableKeyView.as_view(), name="stripe_key"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),
    path("admin/stats/", AdminDashboardStatsView.as_view(), name="admin_stats"),
    path("admin/notifications/", AdminNotificationsView.as_view(), name="admin_notifications"),
    path("", include(router.urls)),
]
