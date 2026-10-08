import os

list_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(list_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('className="mx-auto max-w-[1400px] px-4 pt-32 pb-10 sm:px-6"', 'className="mx-auto max-w-[1400px] px-4 pt-40 pb-10 sm:px-6"')
with open(list_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("ProductListPage.jsx patched")