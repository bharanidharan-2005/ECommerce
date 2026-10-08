import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminProducts.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("icon={FiBox}", "icon={PackageOpen}")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminCustomers.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("icon={FiUsers}", "icon={UsersIcon}")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed icons")
