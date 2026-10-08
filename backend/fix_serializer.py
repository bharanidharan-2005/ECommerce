import re

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\serializers.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'read_only_fields = ("id", "user", "created_at")',
    'read_only_fields = ("id", "user", "created_at", "product")'
)

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\serializers.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ReviewSerializer!")
