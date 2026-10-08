import sys

def fix_file(filepath, bad_pattern, good_pattern):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(bad_pattern, good_pattern)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('src/pages/admin/AdminOrders.jsx', 
         'await api.patch(/orders/admin//', 
         'await api.patch(/orders/admin//')

fix_file('src/pages/admin/AdminProducts.jsx', 
         'await api.delete(/products//', 
         'await api.delete(/products//')
