import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\BentoProductCard.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = """            {/* Stock State */}
            <span className={\text-xs font-bold mt-1 }>
              {product.stock === 0 ? 'Out of Stock' : product.stock <= 5 ? Only  left : 'In Stock'}
            </span>"""

# If the target above doesn't exactly match because of the actual tab character:
target2 = "            <span className={\t" + "ext-xs font-bold mt-1 }>\n              {product.stock === 0 ? 'Out of Stock' : product.stock <= 5 ? Only  left : 'In Stock'}\n            </span>"

replacement = """            {/* Stock State */}
            <span className={`text-xs font-bold mt-1 ${product.stock === 0 ? 'text-rose-400' : product.stock <= 5 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {product.stock === 0 ? 'Out of Stock' : product.stock <= 5 ? `Only ${product.stock} left` : 'In Stock'}
            </span>"""

if target in content:
    content = content.replace(target, replacement)
elif target2 in content:
    content = content.replace(target2, replacement)
else:
    # Try regex fallback
    import re
    content = re.sub(r'\{\/\* Stock State \*\/\}.*?<\/span>', replacement, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed BentoProductCard.jsx')
