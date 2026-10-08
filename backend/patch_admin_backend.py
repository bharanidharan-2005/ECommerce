import os
import re

# 1. Accounts Views - Add AdminNewsletterSubscriberViewSet
accounts_views = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\views.py'
with open(accounts_views, 'r', encoding='utf-8') as f:
    content = f.read()

new_view = '''from rest_framework import viewsets
from rest_framework import serializers

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = '__all__'

class AdminNewsletterSubscriberViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = (permissions.IsAdminUser,)

class NewsletterSubscribeView(APIView):'''

content = content.replace('class NewsletterSubscribeView(APIView):', new_view)
with open(accounts_views, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Accounts URLs - Register the viewset
accounts_urls = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\urls.py'
with open(accounts_urls, 'r', encoding='utf-8') as f:
    urls_content = f.read()

# Make sure not to double add
if 'AdminNewsletterSubscriberViewSet' not in urls_content:
    old_router = 'router.register(r"admin-users", AdminUserViewSet, basename="admin-user")'
    new_router = '''router.register(r"admin-users", AdminUserViewSet, basename="admin-user")
router.register(r"admin-subscribers", AdminNewsletterSubscriberViewSet, basename="admin-subscriber")'''
    urls_content = urls_content.replace(old_router, new_router)
    
    old_import = 'from .views import ('
    new_import = 'from .views import ( AdminNewsletterSubscriberViewSet,'
    urls_content = urls_content.replace(old_import, new_import)
    
    with open(accounts_urls, 'w', encoding='utf-8') as f:
        f.write(urls_content)


print("Backend Admin views patched.")