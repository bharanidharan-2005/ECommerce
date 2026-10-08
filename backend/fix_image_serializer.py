file_path = 'apps/orders/serializers.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_fields = 'fields = ("id", "product_id", "product_name", "price", "quantity", "subtotal")'
new_fields = 'fields = ("id", "product_id", "product_name", "price", "quantity", "subtotal", "image")'
content = content.replace(old_fields, new_fields)

old_readonly = 'read_only_fields = ("id", "product_name", "price", "subtotal")'
new_readonly = 'read_only_fields = ("id", "product_name", "price", "subtotal", "image")'
content = content.replace(old_readonly, new_readonly)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added image to OrderItemSerializer fields.")
