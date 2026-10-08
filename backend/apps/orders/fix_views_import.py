import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from .models import Order", "from .models import Order, PromoCode")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Added PromoCode to views.py imports")
