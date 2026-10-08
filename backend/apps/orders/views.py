import stripe
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, serializers, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, PromoCode
from .serializers import MyOrderSerializer, OrderSerializer


def get_converted_amount(total_price_inr: float, currency_code: str) -> tuple:
    """
    Convert INR amount to target currency using fixed exchange rates.
    Returns (converted_amount_in_cents, currency_code).
    """
    # Base INR
    rates = {
        "INR": 1.0,
        "USD": 96.75,
        "EUR": 108.30,
        "GBP": 128.09
    }
    
    code = currency_code.upper()
    if code not in rates:
        code = "INR"
    
    # 1 USD = 96.75 INR -> USD = INR / 96.75
    converted = total_price_inr / rates[code]
    
    return int(converted * 100), code.lower()
    
    rate_obj = ExchangeRate.objects.filter(currency_code=currency_code).first()
    if rate_obj and rate_obj.rate:
        rate = float(rate_obj.rate)
        converted = total_price_usd * rate
        symbol = rate_obj.symbol
        return int(converted * 100), currency_code
    
    # Fallback to USD if rate not available
    return int(total_price_usd * 100), "usd"



class PromoValidateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response({"detail": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        from apps.accounts.models import NewsletterSubscriber
        from .models import Order
        
        try:
            promo = PromoCode.objects.get(code__iexact=code, active=True)
            if promo.valid_from and promo.valid_from > timezone.now():
                return Response({"detail": "This offer is currently unavailable."}, status=status.HTTP_400_BAD_REQUEST)
            if promo.valid_until and promo.valid_until < timezone.now():
                return Response({"detail": "This coupon has expired."}, status=status.HTTP_400_BAD_REQUEST)
                
            # Newsletter specific check
            subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
            if subscriber and promo.code.upper() == subscriber.welcome_coupon.upper():
                if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                    return Response({"detail": "Your welcome discount has expired."}, status=status.HTTP_400_BAD_REQUEST)
                if subscriber.coupon_used:
                    return Response({"detail": "This coupon has already been used."}, status=status.HTTP_400_BAD_REQUEST)
            elif promo.code.endswith("10") and "WELCOME" not in promo.code:
                # If it looks like a welcome coupon but isn't theirs
                if not subscriber or promo.code.upper() != subscriber.welcome_coupon.upper():
                    # We might want to allow it if it's just a generic coupon, but for username10:
                    pass
            
            # First order check
            if promo.first_order_only:
                if Order.objects.filter(user=request.user).exists():
                    return Response({"detail": "This offer is available for first-time customers only."}, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({
                "code": promo.code,
                "discount_percentage": float(promo.discount_percentage),
                "min_order_amount": float(promo.min_order_amount) if promo.min_order_amount else 0,
                "max_discount_amount": float(promo.max_discount_amount) if promo.max_discount_amount else None
            })
        except PromoCode.DoesNotExist:
            return Response({"detail": "Invalid promo code."}, status=status.HTTP_400_BAD_REQUEST)

class CheckoutView(generics.CreateAPIView):

    """
    POST /api/orders/checkout/
    Creates an order from cart items + shipping address.

    Routing by `payment_method` in the payload:
      - "cod"      -> order saved as PENDING/unpaid; no gateway involved.
                      Response carries no client_secret; frontend goes
                      straight to the success page.
      - "card" | "upi_gpay" | "upi_paytm"
                   -> a Stripe PaymentIntent is created for the total and
                       its client_secret returns for frontend confirmation.
                       The webhook flips the order to PAID on success.
    
    The `currency` field in the payload determines the currency for
    Stripe PaymentIntent. Amount is converted from USD to the target
    currency using cached exchange rates.
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Only accept methods the model knows about
        payment_method = request.data.get("payment_method", Order.PaymentMethod.CARD)
        if payment_method not in Order.PaymentMethod.values:
            payment_method = Order.PaymentMethod.CARD

        # Determine currency: use payload currency or fall back to user's preference
        currency = request.data.get("currency", "")
        if not currency:
            # Try to get from user profile for authenticated users
            if request.user.is_authenticated:
                currency = request.user.currency
        if not currency:
            currency = "USD"
        
        serializer = self.get_serializer(
            data={**request.data, "user": None}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        extra = {"payment_method": payment_method, "currency": currency}
        
        # Process promo code
        promo_code_str = request.data.get("promo_code")
        if promo_code_str:
            from django.utils import timezone
            from decimal import Decimal
            from apps.accounts.models import NewsletterSubscriber
            try:
                promo = PromoCode.objects.get(code__iexact=promo_code_str, active=True)
                if promo.valid_from and promo.valid_from > timezone.now():
                    raise ValueError("This offer is currently unavailable.")
                if promo.valid_until and promo.valid_until < timezone.now():
                    raise ValueError("This coupon has expired.")
                    
                subscriber = NewsletterSubscriber.objects.filter(email=request.user.email).first()
                if subscriber and promo.code.upper() == (subscriber.welcome_coupon or "").upper():
                    if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                        raise ValueError("Your welcome discount has expired.")
                    if subscriber.coupon_used:
                        raise ValueError("This coupon has already been used.")
                elif promo.code.upper() == "WELCOME10":
                    # Fallback for old welcome coupons
                    if not subscriber:
                        raise ValueError("This offer is available for first-time customers only.")
                    if subscriber.coupon_expires_at and subscriber.coupon_expires_at < timezone.now():
                        raise ValueError("Your welcome discount has expired.")
                    if subscriber.coupon_used:
                        raise ValueError("This coupon has already been used.")
                        
                if promo.first_order_only:
                    if Order.objects.filter(user=request.user).exists():
                        raise ValueError("This offer is available for first-time customers only.")
                
                # Calculate subtotal manually to apply discount
                subtotal = Decimal(0)
                from apps.products.models import Product
                for item in request.data.get("items", []):
                    prod = Product.objects.get(pk=item["product_id"])
                    subtotal += prod.price * int(item["quantity"])
                    
                if promo.min_order_amount and subtotal < promo.min_order_amount:
                    raise ValueError(f"This coupon requires a minimum order of ₹{promo.min_order_amount}.")
                
                discount_amount = (subtotal * promo.discount_percentage) / Decimal(100)
                if promo.max_discount_amount and discount_amount > promo.max_discount_amount:
                    discount_amount = promo.max_discount_amount
                    
                extra["promo_code"] = promo
                extra["discount_amount"] = discount_amount
            except PromoCode.DoesNotExist:
                return Response({"detail": "Invalid promo code."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"Invalid promo code: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


        # Capture the UPI VPA so support/ops can trace collect requests
        if payment_method.startswith("upi_"):
            upi_id = (request.data.get("upi_id") or "").strip()
            if not upi_id:
                return Response(
                    {"detail": "A UPI ID is required for GPay/Paytm checkout."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            extra["upi_id"] = upi_id

        order = serializer.save(user=request.user, **extra)

        # Mark welcome coupon as used
        if extra.get("promo_code"):
            from apps.accounts.models import NewsletterSubscriber
            sub = NewsletterSubscriber.objects.filter(email=request.user.email).first()
            if sub and extra["promo_code"].code.upper() in [(sub.welcome_coupon or "").upper(), "WELCOME10"]:
                sub.coupon_used = True
                sub.save(update_fields=['coupon_used'])

        # ---- Cash on delivery: no online charge happens now ----
        if payment_method == Order.PaymentMethod.COD:
            return Response(
                {
                    "order": OrderSerializer(order).data,
                    "client_secret": None,
                    "message": "Order placed. Pay cash on delivery.",
                },
                status=status.HTTP_201_CREATED,
            )

        # ---- Online methods: create a Stripe PaymentIntent ----
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY.startswith("sk_test_xxx"):
            # Demo mode: auto-confirm order since no real gateway keys are set
            order.is_paid = True
            order.status = Order.Status.PAID
            order.paid_at = timezone.now()
            order.save(update_fields=["is_paid", "status", "paid_at"])
            return Response(
                {
                    "order": OrderSerializer(order).data,
                    "client_secret": None,
                    "message": "Order placed and auto-confirmed — demo mode (no gateway keys configured).",
                },
                status=status.HTTP_201_CREATED,
            )

        try:
            converted_amount_cents, currency_code = get_converted_amount(
                float(order.total_price), currency
            )
            intent = stripe.PaymentIntent.create(
                amount=converted_amount_cents,
                currency=currency_code,
                metadata={
                    "order_id": order.id,
                    "order_number": order.order_number,
                    "payment_method": payment_method,
                },
                automatic_payment_methods={"enabled": True},
            )
        except stripe.error.StripeError as exc:
            return Response(
                {"detail": f"Payment gateway error: {exc.user_message or exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        order.stripe_payment_intent_id = intent.id
        order.save(update_fields=["stripe_payment_intent_id"])

        return Response(
            {
                "order": OrderSerializer(order).data,
                "client_secret": intent.client_secret,
                "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
            },
            status=status.HTTP_201_CREATED,
        )


class StripeWebhookView(APIView):
    """POST /api/orders/stripe/webhook/ - marks orders paid on success events."""
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            order = Order.objects.filter(
                stripe_payment_intent_id=intent["id"]
            ).first()
            if order:
                order.is_paid = True
                order.status = Order.Status.PAID
                order.paid_at = timezone.now()
                order.save(update_fields=["is_paid", "status", "paid_at"])

        return Response(status=status.HTTP_200_OK)


class StripePublishableKeyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({"publishableKey": settings.STRIPE_PUBLISHABLE_KEY})


class MyOrdersView(generics.ListAPIView):
    """GET /api/orders/my/ - authenticated user's order history."""
    serializer_class = MyOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
        )

from rest_framework.viewsets import ModelViewSet
class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'

class AdminPromoCodeViewSet(ModelViewSet):
    serializer_class = PromoCodeSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = PromoCode.objects.all().order_by('-id')

class AdminOrderViewSet(viewsets.ModelViewSet):
    """Admin view to list all orders and update statuses."""
    queryset = Order.objects.all().order_by('-created_at').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_update(self, serializer):
        status_val = self.request.data.get('status')
        instance = serializer.instance
        old_status = instance.status
        from django.utils import timezone
        from django.db import transaction
        
        kwargs = {}
        if status_val:
            if status_val == 'delivered':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
            elif status_val == 'paid':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
                    
        with transaction.atomic():
            serializer.save(**kwargs)
            # If status changed to cancelled from a non-cancelled state, restore stock
            if status_val == 'cancelled' and old_status != 'cancelled':
                for item in instance.items.all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save(update_fields=['stock'])
            # If status changed from cancelled to another state, deduce stock
            elif old_status == 'cancelled' and status_val and status_val != 'cancelled':
                for item in instance.items.all():
                    if item.product:
                        item.product.stock -= item.quantity
                        if item.product.stock < 0:
                            item.product.stock = 0
                        item.product.save(update_fields=['stock'])

    def update(self, request, *args, **kwargs):
        # We might want to allow partial updates specifically for 'status', 'is_paid', 'is_delivered'
        return super().update(request, *args, **kwargs)

class AdminDashboardStatsView(APIView):
    """Returns aggregated stats for the admin dashboard."""
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        from django.db.models import Sum, Count, Q
        from django.contrib.auth import get_user_model
        from apps.products.models import Product
        from django.utils import timezone
        from datetime import timedelta
        
        total_orders = Order.objects.count()
        # Include both is_paid=True and status='delivered' (for COD orders)
        revenue = Order.objects.filter(Q(is_paid=True) | Q(status='delivered')).aggregate(total=Sum('total_price'))['total'] or 0
        User = get_user_model()
        total_users = User.objects.count()
        total_products = Product.objects.count()

        # Status breakdown for Pie Chart
        status_counts = Order.objects.values('status').annotate(count=Count('id'))
        status_data = [{"name": item['status'].capitalize(), "value": item['count']} for item in status_counts]

        try:
            days = int(request.GET.get('days', 7))
        except ValueError:
            days = 7

        # Last days days revenue for Line/Bar Chart
        today = timezone.now().date()
        sales_data = []
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            # Find all paid orders on this day
            day_orders_qs = Order.objects.filter(created_at__date=day)
            day_revenue = day_orders_qs.filter(
                Q(is_paid=True) | Q(status='delivered')
            ).aggregate(total=Sum('total_price'))['total'] or 0
            day_orders_count = day_orders_qs.count()
            day_paid = day_orders_qs.filter(is_paid=True).count()
            day_delivered = day_orders_qs.filter(status='delivered').count()
            day_pending = day_orders_qs.filter(status='pending').count()
            
            sales_data.append({
                "date": day.strftime("%b %d" if days <= 31 else "%Y-%m-%d"),
                "revenue": float(day_revenue),
                "orders": day_orders_count,
                "paid": day_paid,
                "delivered": day_delivered,
                "pending": day_pending
            })

        return Response({
            'total_orders': total_orders,
            'total_revenue': float(revenue),
            'total_users': total_users,
            'total_products': total_products,
            'status_data': status_data,
            'sales_data': sales_data,
        })

class AdminNotificationsView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        from apps.products.models import Product
        from apps.orders.models import Order
        from django.utils import timezone
        
        notifications = []
        
        # 1. Low stock alerts
        low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)[:5]
        for p in low_stock_products:
            notifications.append({
                "id": f"p_{p.id}",
                "title": "Low Stock Alert",
                "desc": f"Product '{p.name}' is running low (Stock: {p.stock}).",
                "time": p.updated_at.isoformat(),
                "unread": True,
                "type": "stock"
            })
            
        # 2. Recent pending orders
        recent_orders = Order.objects.filter(status=Order.Status.PENDING).order_by('-created_at')[:5]
        for o in recent_orders:
            notifications.append({
                "id": f"o_{o.id}",
                "title": f"New Order #{o.id}",
                "desc": f"Pending order from {o.full_name or o.email}.",
                "time": o.created_at.isoformat(),
                "unread": True,
                "type": "order"
            })
            
        # Sort by time descending
        notifications.sort(key=lambda x: x["time"], reverse=True)
        
        return Response(notifications[:10])

class CancelOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request, pk):
        from apps.orders.models import Order
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            if order.status in [Order.Status.PENDING, Order.Status.PAID]:
                order.status = Order.Status.CANCELLED
                order.save(update_fields=['status'])
                # Restore stock
                for item in order.items.all():
                    if item.product:
                        item.product.stock += item.quantity
                        item.product.save(update_fields=['stock'])
                return Response({"detail": "Order cancelled successfully."})
            return Response({"detail": "Cannot cancel this order."}, status=400)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)
