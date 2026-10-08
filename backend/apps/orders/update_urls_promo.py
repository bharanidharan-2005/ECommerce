import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\urls.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

if "AdminPromoCodeViewSet" not in content:
    content = content.replace("    AdminOrderViewSet,", "    AdminOrderViewSet,\n    AdminPromoCodeViewSet,")
    content = content.replace("router.register(r\"admin\", AdminOrderViewSet, basename=\"admin-orders\")", 'router.register(r"admin", AdminOrderViewSet, basename="admin-orders")\nrouter.register(r"admin-promos", AdminPromoCodeViewSet, basename="admin-promos")')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated urls.py with AdminPromoCodeViewSet")
