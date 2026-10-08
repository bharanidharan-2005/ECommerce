import os

views_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\views.py"

with open(views_path, "r", encoding="utf-8") as f:
    content = f.read()

new_view = """
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

"""

if "class UpdateCouponView" not in content:
    content += new_view
    with open(views_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added UpdateCouponView to views.py")


urls_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

if "UpdateCouponView" not in urls_content:
    urls_content = urls_content.replace(
        "from .views import (",
        "from .views import (\n    UpdateCouponView,"
    )
    urls_content = urls_content.replace(
        "urlpatterns = [",
        "urlpatterns = [\n    path('profile/coupon/', UpdateCouponView.as_view(), name='profile-coupon'),"
    )
    with open(urls_path, "w", encoding="utf-8") as f:
        f.write(urls_content)
    print("Added URL for UpdateCouponView")

