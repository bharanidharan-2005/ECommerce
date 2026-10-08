import os

accounts_urls = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\accounts\urls.py'
with open(accounts_urls, 'r', encoding='utf-8') as f:
    content = f.read()

if 'admin-subscribers' not in content:
    new_import = 'from .views import LoginView, ProfileView, RegisterView, AdminCustomerListView, StoreSettingsView, NewsletterSubscribeView, AdminNewsletterSubscriberViewSet'
    content = content.replace('from .views import LoginView, ProfileView, RegisterView, AdminCustomerListView, StoreSettingsView, NewsletterSubscribeView', new_import)
    
    new_path = "path('admin-subscribers/', AdminNewsletterSubscriberViewSet.as_view({'get': 'list'}), name='admin-subscribers'),"
    content = content.replace('path("admin/customers/", AdminCustomerListView.as_view(), name="admin_customers"),', 'path("admin/customers/", AdminCustomerListView.as_view(), name="admin_customers"),\n    ' + new_path)
    
    with open(accounts_urls, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("accounts URLs updated")