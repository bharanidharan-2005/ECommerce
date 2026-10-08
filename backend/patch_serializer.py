import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\serializers.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """        fields = (
            "id", "order_number", "status", "items", "total_price",
            "is_paid", "created_at",
        )"""

replacement = """        fields = (
            "id", "order_number", "status", "items", "total_price",
            "is_paid", "created_at", "full_name", "email",
            "address_line_1", "address_line_2", "city", "state",
            "postal_code", "country", "payment_method",
        )"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
