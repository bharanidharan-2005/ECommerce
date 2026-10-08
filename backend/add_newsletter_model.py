import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

models_path = 'apps/accounts/models.py'
model_code = '''

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
'''

with open(models_path, 'a') as f:
    f.write(model_code)

print('Model appended successfully')
