import os

models_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\models.py"

with open(models_path, "r", encoding="utf-8") as f:
    content = f.read()

if "class StoreSetting(" not in content:
    content += """

class StoreSetting(models.Model):
    settings = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Store Settings"

    def __str__(self):
        return "Global Store Settings"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        if created or not obj.settings:
            obj.settings = {
                "storeName": "ShopVerse",
                "storeEmail": "contact@shopverse.com",
                "supportEmail": "support@shopverse.com",
                "phone": "+91 9876543210",
                "description": "Premium E-commerce Store",
                "storeStatus": "open",
                "closureMessage": "We are temporarily closed.",
                "currency": "INR",
                "country": "India",
                "timezone": "Asia/Kolkata",
                "language": "English",
                "dateFormat": "DD/MM/YYYY",
                "numberFormat": "Indian",
                "emailNotifications": True,
                "inAppNotifications": True,
                "legalBusinessName": "ShopVerse Technologies Pvt Ltd",
                "gstin": "22AAAAA0000A1Z5",
                "pan": "ABCDE1234F",
                "businessAddress": "123 Tech Park",
                "city": "Bangalore",
                "state": "Karnataka",
                "pinCode": "560001",
                "orderIdPrefix": "ORD",
                "autoCancelUnpaid": True,
                "cancelAfterHours": 24,
                "shippingEnabled": True,
                "flatRate": 50,
                "freeShippingThreshold": 500,
                "taxEnabled": True,
                "defaultTaxRate": 18,
                "pricesIncludeTax": False,
                "returnsEnabled": True,
                "returnWindowDays": 7,
            }
            obj.save()
        return obj
"""
    with open(models_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Added StoreSetting model")
