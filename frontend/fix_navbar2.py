import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

desktop_target = 'Categories <FiChevronDown size={14} className={	ransition-transform } />'
desktop_replacement = '{currentCategoryLabel} <FiChevronDown size={14} className={	ransition-transform } />'

mobile_target = '<span>Categories</span>'
mobile_replacement = '<span>{currentCategoryLabel}</span>'

# Because "Categories" is used inside the <span>Categories</span>, let's replace only the 1st match in the mobile block
# But wait, we can just replace 'Categories <FiChevronDown size={14}'
t1 = 'Categories <FiChevronDown size={14}'
r1 = '{currentCategoryLabel} <FiChevronDown size={14}'
content = content.replace(t1, r1)

t2 = '<span>Categories</span>\n                  <FiChevronDown size={18}'
r2 = '<span>{currentCategoryLabel}</span>\n                  <FiChevronDown size={18}'
content = content.replace(t2, r2)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed Navbar Labels.')
