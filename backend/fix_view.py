import re

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\views.py", "r", encoding="utf-8") as f:
    content = f.read()

old_perform_create = """    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs["product_pk"])
        serializer.save(user=self.request.user, product=product)"""

new_perform_create = """    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        from django.db import IntegrityError
        product = Product.objects.get(pk=self.kwargs["product_pk"])
        try:
            serializer.save(user=self.request.user, product=product)
        except IntegrityError:
            raise ValidationError({"non_field_errors": ["You have already reviewed this product."]})"""

content = content.replace(old_perform_create, new_perform_create)

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\products\views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ReviewViewSet!")
