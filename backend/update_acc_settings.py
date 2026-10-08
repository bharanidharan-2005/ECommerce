import os

views_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\views.py"

with open(views_path, "r", encoding="utf-8") as f:
    content = f.read()

if "StoreSettingsView" not in content:
    content += """
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreSetting

class StoreSettingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        store_settings = StoreSetting.get_settings()
        return Response(store_settings.settings)
        
    def patch(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Not authorized"}, status=403)
        store_settings = StoreSetting.get_settings()
        store_settings.settings.update(request.data)
        store_settings.save()
        return Response(store_settings.settings)
"""
    with open(views_path, "w", encoding="utf-8") as f:
        f.write(content)

urls_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

if "StoreSettingsView" not in urls_content:
    urls_content = urls_content.replace(
        "from .views import RegisterView, LoginView, ProfileView, AdminCustomerListView", 
        "from .views import RegisterView, LoginView, ProfileView, AdminCustomerListView, StoreSettingsView"
    )
    urls_content = urls_content.replace(
        "urlpatterns = [",
        "urlpatterns = [\n    path('settings/', StoreSettingsView.as_view(), name='store-settings'),"
    )
    with open(urls_path, "w", encoding="utf-8") as f:
        f.write(urls_content)

print("Updated views and urls for settings")
