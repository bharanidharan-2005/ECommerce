import os

file_path = 'apps/orders/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace AdminDashboardStatsView
old_stats = """    def get(self, request):
        from django.db.models import Sum, Count
        from django.contrib.auth import get_user_model
        from apps.products.models import Product
        from django.utils import timezone
        from datetime import timedelta
        
        total_orders = Order.objects.count()
        revenue = Order.objects.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0"""

new_stats = """    def get(self, request):
        from django.db.models import Sum, Count, Q
        from django.contrib.auth import get_user_model
        from apps.products.models import Product
        from django.utils import timezone
        from datetime import timedelta
        
        total_orders = Order.objects.count()
        # Include both is_paid=True and status='delivered' (for COD orders)
        revenue = Order.objects.filter(Q(is_paid=True) | Q(status='delivered')).aggregate(total=Sum('total_price'))['total'] or 0"""

content = content.replace(old_stats, new_stats)

old_daily_rev = """            # Find all paid orders on this day
            day_revenue = Order.objects.filter(
                is_paid=True, 
                created_at__date=day
            ).aggregate(total=Sum('total_price'))['total'] or 0"""

new_daily_rev = """            # Find all paid orders on this day
            day_revenue = Order.objects.filter(
                Q(is_paid=True) | Q(status='delivered'), 
                created_at__date=day
            ).aggregate(total=Sum('total_price'))['total'] or 0"""

content = content.replace(old_daily_rev, new_daily_rev)


old_admin_update = """    def update(self, request, *args, **kwargs):
        # We might want to allow partial updates specifically for 'status', 'is_paid', 'is_delivered'
        return super().update(request, *args, **kwargs)"""

new_admin_update = """    def perform_update(self, serializer):
        status_val = self.request.data.get('status')
        instance = serializer.instance
        from django.utils import timezone
        
        kwargs = {}
        if status_val:
            if status_val == 'delivered':
                if not instance.is_delivered:
                    kwargs['is_delivered'] = True
                    kwargs['delivered_at'] = timezone.now()
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
            elif status_val == 'paid':
                if not instance.is_paid:
                    kwargs['is_paid'] = True
                    kwargs['paid_at'] = timezone.now()
                    
        serializer.save(**kwargs)

    def update(self, request, *args, **kwargs):
        # We might want to allow partial updates specifically for 'status', 'is_paid', 'is_delivered'
        return super().update(request, *args, **kwargs)"""

content = content.replace(old_admin_update, new_admin_update)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed revenue calculation and admin order update logic.")
