import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\models.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)'''
replacement = '''    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated models.py')
else:
    print('Could not find target in models.py')
