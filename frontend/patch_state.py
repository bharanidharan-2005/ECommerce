import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'const [page, setPage] = useState(1);'
replacement = '''const [minPrice, setMinPrice] = useState(searchParams.get("minPrice") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("maxPrice") || "");
  const [inStock, setInStock] = useState(searchParams.get("inStock") === "true");
  const [page, setPage] = useState(1);'''

new_content = content.replace(target, replacement)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Patched ProductListPage.jsx state')
