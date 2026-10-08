file_path = 'apps/orders/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We need to replace the AdminDashboardStatsView get method
old_stats = '''    def get(self, request):
        total_orders = Order.objects.count()
        
        # calculate total revenue (only paid orders)
        from django.db.models import Sum
        revenue = Order.objects.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0

        # total users
        from django.contrib.auth import get_user_model
        User = get_user_model()
        total_users = User.objects.count()

        # total products
        from apps.products.models import Product
        total_products = Product.objects.count()

        return Response({
            'total_orders': total_orders,
            'total_revenue': float(revenue),
            'total_users': total_users,
            'total_products': total_products,
        })'''

new_stats = '''    def get(self, request):
        from django.db.models import Sum, Count
        from django.contrib.auth import get_user_model
        from apps.products.models import Product
        from django.utils import timezone
        from datetime import timedelta
        
        total_orders = Order.objects.count()
        revenue = Order.objects.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0
        User = get_user_model()
        total_users = User.objects.count()
        total_products = Product.objects.count()

        # Status breakdown for Pie Chart
        status_counts = Order.objects.values('status').annotate(count=Count('id'))
        status_data = [{"name": item['status'].capitalize(), "value": item['count']} for item in status_counts]

        # Last 7 days revenue for Line/Bar Chart
        today = timezone.now().date()
        sales_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            # Find all paid orders on this day
            day_revenue = Order.objects.filter(
                is_paid=True, 
                created_at__date=day
            ).aggregate(total=Sum('total_price'))['total'] or 0
            sales_data.append({
                "date": day.strftime("%b %d"),
                "revenue": float(day_revenue)
            })

        return Response({
            'total_orders': total_orders,
            'total_revenue': float(revenue),
            'total_users': total_users,
            'total_products': total_products,
            'status_data': status_data,
            'sales_data': sales_data,
        })'''

content = content.replace(old_stats, new_stats)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated AdminDashboardStatsView')
