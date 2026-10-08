import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

viewset = """
from rest_framework.viewsets import ModelViewSet
class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'

class AdminPromoCodeViewSet(ModelViewSet):
    serializer_class = PromoCodeSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = PromoCode.objects.all().order_by('-id')
"""

if "AdminPromoCodeViewSet" not in content:
    content = content.replace("class AdminOrderViewSet", viewset + "\nclass AdminOrderViewSet")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Added AdminPromoCodeViewSet to views.py")
