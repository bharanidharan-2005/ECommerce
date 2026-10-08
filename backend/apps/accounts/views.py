from rest_framework import generics, permissions
from django.db.models import Count
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, NewsletterSubscriber
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer, AdminCustomerSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AdminCustomerListView(generics.ListAPIView):
    serializer_class = AdminCustomerSerializer
    permission_classes = (permissions.IsAuthenticated,) # In real app, IsAdminUser

    def get_queryset(self):
        return User.objects.annotate(orders_count=Count('orders')).order_by('-date_joined')

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreSetting

class StoreSettingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        store_settings = StoreSetting.get_settings()
        return Response(store_settings.settings)
        
    def patch(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Not authorized"}, status=403)
        store_settings = StoreSetting.get_settings()
        store_settings.settings.update(request.data)
        store_settings.save()
        return Response(store_settings.settings)

from .models import NewsletterSubscriber

from rest_framework import viewsets
from rest_framework import serializers

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'

class AdminNewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = (permissions.IsAdminUser,)

class NewsletterSubscribeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)
        
        from datetime import timedelta
        from django.utils import timezone
        
        subscriber = NewsletterSubscriber.objects.filter(email=email).first()
        if subscriber:
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
            return Response({"message": "You're already subscribed to ShopVerse."}, status=400)
            
        expires_at = timezone.now() + timedelta(days=7)
        username = email.split('@')[0]
        username = ''.join(e for e in username if e.isalnum())
        if not username:
            username = "USER"
        coupon_code = f"{username}10".upper()
        
        from apps.orders.models import PromoCode
        promo, created = PromoCode.objects.get_or_create(
            code=coupon_code,
            defaults={'discount_percentage': 10, 'active': True}
        )

        subscriber = NewsletterSubscriber.objects.create(
            email=email,
            welcome_coupon=coupon_code,
            coupon_expires_at=expires_at
        )
            
        return Response({
            "message": "Successfully subscribed!",
            "coupon": coupon_code,
            "expires_at": expires_at.isoformat(),
            "discount_percentage": 10,
            "min_order": 999
        }, status=201)

class UpdateCouponView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
        if subscriber and subscriber.welcome_coupon:
            return Response({"coupon": subscriber.welcome_coupon})
        return Response({"coupon": None})

    def put(self, request):
        new_coupon = request.data.get("coupon")
        if not new_coupon:
            return Response({"error": "Coupon code is required"}, status=400)
            
        new_coupon = new_coupon.strip().upper()
        
        subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
        if not subscriber:
            return Response({"error": "You are not subscribed to the newsletter. Subscribe to get a custom coupon."}, status=400)
            
        old_coupon = subscriber.welcome_coupon.upper() if subscriber.welcome_coupon else ""
        
        from apps.orders.models import PromoCode
        # Check if the new coupon already exists and is owned by someone else
        if PromoCode.objects.filter(code__iexact=new_coupon).exclude(code__iexact=old_coupon).exists():
            return Response({"error": "This coupon code is already taken"}, status=400)
            
        # Update PromoCode
        if old_coupon:
            promo = PromoCode.objects.filter(code__iexact=old_coupon).first()
            if promo:
                promo.code = new_coupon
                promo.save()
            else:
                PromoCode.objects.create(code=new_coupon, discount_percentage=10.00, active=True)
        else:
            PromoCode.objects.create(code=new_coupon, discount_percentage=10.00, active=True)
            
        # Update Subscriber
        subscriber.welcome_coupon = new_coupon
        subscriber.save()
        
        return Response({"message": "Coupon updated successfully", "coupon": new_coupon})

