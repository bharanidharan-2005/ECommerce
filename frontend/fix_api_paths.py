import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'await api.get("/accounts/profile/coupon/");',
    'await api.get("/auth/profile/coupon/");'
)
content = content.replace(
    'await api.put("/accounts/profile/coupon/", { coupon });',
    'await api.put("/auth/profile/coupon/", { coupon });'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated API endpoints in ProfilePage.jsx")
