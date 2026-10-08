import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product

# 1. Update Categories
cat_audio, _ = Category.objects.get_or_create(id=2)
cat_audio.name = 'Audio'
cat_audio.slug = 'audio'
cat_audio.save()

cat_smart, _ = Category.objects.get_or_create(id=3)
cat_smart.name = 'Smart Devices'
cat_smart.slug = 'smart-devices'
cat_smart.save()

cat_accessories, _ = Category.objects.get_or_create(id=5)
cat_accessories.name = 'Computer Accessories'
cat_accessories.slug = 'computer-accessories'
cat_accessories.save()

print('Categories updated.')

# 2. Update Products in Audio (formerly Fashion)
audio_names = [
    'Studio Reference Headphones', 'Wireless Earbuds Active', 
    'Bluetooth Portable Speaker', 'Soundbar with Subwoofer',
    'USB Condenser Microphone', 'Audiophile DAC/Amp',
    'Gaming Headset 7.1', 'Noise-Cancelling Headphones',
    'True Wireless Earbuds Pro', 'Audio Interface 2x2'
]

fashion_products = Product.objects.filter(category=cat_audio)
for i, p in enumerate(fashion_products):
    if i < len(audio_names):
        p.name = audio_names[i]
        p.slug = p.name.lower().replace(' ', '-') + f'-{p.id}'
        p.description = f'Premium {p.name} for the best audio experience.'
        p.save()

# 3. Update Products in Smart Devices (formerly Home)
smart_names = [
    'Smart Home Hub', 'Wi-Fi Security Camera',
    'Smart Thermostat V2', 'Robot Vacuum cleaner Pro',
    'Smart LED Light Strip', 'Video Doorbell',
    'Smart Plugs (4-Pack)', 'Mesh Wi-Fi System',
    'Smart Smoke Detector', 'Smart Lock Pro',
    'Smart Display 10-inch'
]

home_products = Product.objects.filter(category=cat_smart)
for i, p in enumerate(home_products):
    if i < len(smart_names):
        p.name = smart_names[i]
        p.slug = p.name.lower().replace(' ', '-') + f'-{p.id}'
        p.description = f'Upgrade your home with {p.name}.'
        p.save()

# 4. Update Products in Computer Accessories (formerly Accessories)
acc_names = [
    'Ergonomic Mechanical Keyboard', 'Wireless Ergonomic Mouse',
    'USB-C Multiport Adapter', 'Laptop Stand Aluminum',
    'Large Desk Mat', 'Webcam 4K Ultra HD',
    'Dual Monitor Mount'
]

acc_products = Product.objects.filter(category=cat_accessories)
for i, p in enumerate(acc_products):
    if i < len(acc_names):
        p.name = acc_names[i]
        p.slug = p.name.lower().replace(' ', '-') + f'-{p.id}'
        p.description = f'High quality {p.name} for your workstation.'
        p.save()

# 5. Fix Gaming products that were weird (e.g. Yoga Mat, Foam Roller, Stand Up Paddleboard)
gaming_products = Product.objects.filter(category__name='Gaming')
gaming_fixes = [
    'RGB Gaming Mousepad', 'Gaming Chair Ergonomic',
    'Mechanical Switch Tester', 'Gaming Controller Pro',
    'VR Headset Elite', 'Stream Deck Mini',
    'Capture Card 4K', 'Gaming Router AX11000',
    'RGB Light Bars', 'Microphone Boom Arm',
    'Gaming Console 2TB'
]
count = 0
for p in gaming_products:
    if 'Yoga' in p.name or 'Foam' in p.name or 'Paddleboard' in p.name or 'Jump' in p.name or 'Tennis' in p.name or 'Tent' in p.name or 'Water Bottle' in p.name or 'Backpack' in p.name or 'Dumbbell' in p.name or 'Shoe' in p.name or 'Sleeve' in p.name or 'Gloves' in p.name or 'Towel' in p.name or 'Band' in p.name or 'Helmet' in p.name:
        if count < len(gaming_fixes):
            p.name = gaming_fixes[count]
            p.slug = p.name.lower().replace(' ', '-') + f'-{p.id}'
            p.description = f'Level up your setup with {p.name}.'
            p.save()
            count += 1

print('Products updated to match tech theme.')
