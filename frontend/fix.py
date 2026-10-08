file_path = 'src/pages/admin/AdminOrders.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'await api.patch(\"/orders/\" + orderId + \"/update_status/\", { status: newStatus });',
    'await api.patch(\"/orders/admin/\" + orderId + \"/\", { status: newStatus });'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated AdminOrders.jsx')
