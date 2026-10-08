import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

filter_code = '''import django_filters

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['category']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

@method_decorator(cache_page(60 * 15), name='list')
class ProductViewSet(viewsets.ModelViewSet):'''

target_string = '''@method_decorator(cache_page(60 * 15), name='list')
class ProductViewSet(viewsets.ModelViewSet):'''

new_content = content.replace(target_string, filter_code)
new_content = new_content.replace('filterset_fields = ("category",)', 'filterset_class = ProductFilter')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Updated views.py with ProductFilter')
