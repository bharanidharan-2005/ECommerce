from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UpdateCouponView, PasswordChangeView, LoginView, ProfileView, RegisterView, AdminCustomerListView, StoreSettingsView, NewsletterSubscribeView, AdminNewsletterSubscriberViewSet

urlpatterns = [
    path('profile/coupon/', UpdateCouponView.as_view(), name='profile-coupon'),
    path('settings/', StoreSettingsView.as_view(), name='store-settings'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("admin/customers/", AdminCustomerListView.as_view(), name="admin_customers"),
    path('admin-subscribers/', AdminNewsletterSubscriberViewSet.as_view({'get': 'list'}), name='admin-subscribers'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
]