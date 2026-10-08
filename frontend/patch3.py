import sys

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('await api.patch(/orders/admin//, { status: newStatus });', 'await api.patch(/orders/admin//, { status: newStatus });')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('src/pages/admin/AdminOrders.jsx')

def fix_file2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('await api.delete(/products//);', 'await api.delete(/products//);')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file2('src/pages/admin/AdminProducts.jsx')
