import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''async({ page = 1, search = "", category = "", ordering = "" }, { rejectWithValue }) => {
try {
const params = { page };
if (search) params.search = search;
if (category) params.category = category;
if (ordering) params.ordering = ordering;'''

replacement = '''async({ page = 1, search = "", category = "", ordering = "", minPrice, maxPrice, inStock }, { rejectWithValue }) => {
try {
const params = { page };
if (search) params.search = search;
if (category) params.category = category;
if (ordering) params.ordering = ordering;
if (minPrice) params.min_price = minPrice;
if (maxPrice) params.max_price = maxPrice;
if (inStock) params.in_stock = true;'''

new_content = content.replace(target, replacement)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Patched productsSlice.js')
