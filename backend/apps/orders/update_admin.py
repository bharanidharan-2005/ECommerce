import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\admin.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

if "PromoCode" not in content:
    content = content.replace("from .models import Order, OrderItem", "from .models import Order, OrderItem, PromoCode")
    promo_admin = """
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percentage", "active", "valid_from", "valid_until")
    list_filter = ("active",)
    search_fields = ("code",)
"""
    content += promo_admin

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py with PromoCode")
