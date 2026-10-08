import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\models.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

promo_code_model = """
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount in percentage (e.g. 10.00 for 10%)")
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"

class Order(models.Model):
"""

if "class PromoCode" not in content:
    content = content.replace("class Order(models.Model):", promo_code_model)

order_fields = """
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
"""

if "promo_code =" not in content:
    content = content.replace("    total_price = models.DecimalField(max_digits=10, decimal_places=2)\n    is_paid = models.BooleanField(default=False)", order_fields)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated orders/models.py with PromoCode")
