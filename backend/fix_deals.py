import sys
import re

# 1. Update HomePage.jsx to remove underline
home_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\HomePage.jsx'
with open(home_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

home_content = home_content.replace(
    'className="border-y border-slate-800 bg-slate-900/50 backdrop-blur"',
    'className="bg-slate-900/50 backdrop-blur"'
)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(home_content)


# 2. Update views.py to handle "sale=true"
views_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

views_target = '''class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['category']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset'''

views_replacement = '''class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    sale = django_filters.BooleanFilter(method='filter_sale')

    class Meta:
        model = Product
        fields = ['category']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
        
    def filter_sale(self, queryset, name, value):
        if value:
            # Fake "deals" logic: Return products under a specific price threshold (e.g. 500)
            return queryset.filter(price__lte=1000)
        return queryset'''

views_content = views_content.replace(views_target, views_replacement)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

print('Updated HomePage.jsx and views.py')
