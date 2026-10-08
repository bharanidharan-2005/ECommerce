import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    def filter_sale(self, queryset, name, value):
        if value:
            # Fake "deals" logic: Return products under a specific price threshold (e.g. 500)
            return queryset.filter(price__lte=1000)
        return queryset'''

replacement = '''    def filter_sale(self, queryset, name, value):
        from django.db.models import F
        if value:
            return queryset.filter(original_price__isnull=False, original_price__gt=F('price'))
        return queryset'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated views.py')
else:
    print('Could not find target in views.py')
