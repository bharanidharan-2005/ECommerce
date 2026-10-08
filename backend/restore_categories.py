from apps.products.models import Category, Product
import re

# 1. Update Categories
cat2, _ = Category.objects.get_or_create(id=2)
cat2.name = 'Fashion'
cat2.slug = 'fashion'
cat2.save()

cat3, _ = Category.objects.get_or_create(id=3)
cat3.name = 'Home'
cat3.slug = 'home'
cat3.save()

cat4, _ = Category.objects.get_or_create(id=4)
cat4.name = 'Sports'
cat4.slug = 'sports'
cat4.save()

cat5, _ = Category.objects.get_or_create(id=5)
cat5.name = 'Accessories'
cat5.slug = 'accessories'
cat5.save()

print('Categories restored.')

def prettify_name(image_str):
    # e.g. 'products/satin_pillowcase_set_1790613982046.jpg' -> 'satin pillowcase set'
    name = image_str.replace('products/', '').replace('.jpg', '').replace('.png', '').replace('.webp', '')
    # remove trailing numbers like _1790613982046
    name = re.sub(r'_[0-9]{10,}.*$', '', name)
    name = name.replace('-', ' ').replace('_', ' ')
    name = name.replace(' fixed', '').replace(' new', '')
    return name.title()

for cat_id in [2, 3, 4, 5]:
    prods = Product.objects.filter(category_id=cat_id)
    for p in prods:
        image_name = p.image.name if p.image else ''
        if image_name:
            p.name = prettify_name(image_name)
            p.slug = p.name.lower().replace(' ', '-') + f'-{p.id}'
            p.save()

print('Products restored based on images.')
