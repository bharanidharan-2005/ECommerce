import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\urls.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Add PromoValidateView to imports
old_import = "    CancelOrderView,\n)"
new_import = "    CancelOrderView,\n    PromoValidateView,\n)"
content = content.replace(old_import, new_import)

# Add URL pattern
old_url = '    path("checkout/", CheckoutView.as_view(), name="checkout"),'
new_url = '    path("checkout/", CheckoutView.as_view(), name="checkout"),\n    path("promo/validate/", PromoValidateView.as_view(), name="promo_validate"),'
content = content.replace(old_url, new_url)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated urls.py with promo validation endpoint")
