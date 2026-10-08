import re

file_path = "backend/apps/orders/views.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I want to add order count per day to sales_data
old_sales_data_loop = """
          for i in range(6, -1, -1):
              day = today - timedelta(days=i)
              # Find all paid orders on this day
              day_revenue = Order.objects.filter(
                  Q(is_paid=True) | Q(status='delivered'), 
                  created_at__date=day
              ).aggregate(total=Sum('total_price'))['total'] or 0
              sales_data.append({
                  "date": day.strftime("%b %d"),
                  "revenue": float(day_revenue)
              })
"""

new_sales_data_loop = """
          for i in range(6, -1, -1):
              day = today - timedelta(days=i)
              
              # Find all paid orders on this day for revenue
              day_revenue = Order.objects.filter(
                  Q(is_paid=True) | Q(status='delivered'), 
                  created_at__date=day
              ).aggregate(total=Sum('total_price'))['total'] or 0
              
              # Find all orders created on this day for order volume
              day_orders = Order.objects.filter(created_at__date=day).count()
              
              sales_data.append({
                  "date": day.strftime("%b %d"),
                  "revenue": float(day_revenue),
                  "orders": day_orders
              })
"""

content = content.replace(old_sales_data_loop.strip(), new_sales_data_loop.strip())

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated backend to include daily orders volume")
