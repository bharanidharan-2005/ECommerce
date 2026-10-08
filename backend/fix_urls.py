import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\urls.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "from .views import LoginView",
    "from .views import UpdateCouponView, LoginView"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated urls.py with UpdateCouponView import")
