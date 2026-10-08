import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminPromos.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'const { data } = const payload = { ...newPromo };', 
    'const payload = { ...newPromo };'
).replace(
    'await api.post("/orders/admin-promos/", payload);',
    'const { data } = await api.post("/orders/admin-promos/", payload);'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed AdminPromos.jsx')
