import os
import django
import requests
from bs4 import BeautifulSoup

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from apps.products.models import Product
from django.conf import settings

media_root = settings.MEDIA_ROOT
products_dir = os.path.join(media_root, 'products')
os.makedirs(products_dir, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

product_mapping = {
    "Tablet Stand": "https://eu.ugreen.com/cdn/shop/files/ugreen-tablet-stand-holder-for-desk-height-adjustable-aluminum-560164.png?v=1747818844&width=720",
    "E-Reader": "https://assets.kogan.com/images/techcrazy/TZY-CT01599/1-02b23e69ba-amazon-kindle-_2022_-6-inch-ct01599.jpg",
    "Bicycle Helmet": "https://www.adoebike.com/cdn/shop/files/3-2.jpg?v=1723540087",
    "Cotton Crewneck Sweater": "https://www.jcrew.com/s7-img-facade/CQ757_BL8133?crop=0%2C0%2C1024%2C0&hei=1280",
    "Polarized Aviator Sunglasses": "https://cdn11.bigcommerce.com/s-3kam1hz68o/images/stencil/200x200/products/61324/137237/0RB3025019W358__63054.1677686405.jpg?c=1",
    "Canvas Weekend Duffel": "https://www.unihandmade.com/products/canvas-duffel-bag-with-shoes-compartment-canvas-weekend-overnight-bag",
    "Minimalist Desk Lamp": "https://www.canadiantire.ca/en/pdp/noma-led-minimalist-desk-lamp-with-wireless-charging-16-7-in-black-0529783p.html",
    "4K Action Camera": "https://www.spritegroup.com/images/products/B10/sprite-group-9x-action-camera-back-screen-display.jpg",
    "37-in-1 Sensor Kit": "https://www.electropi.in/image/cache/catalog/37-in-1-sensor-module-kit-for-arduino-800x800.jpg",
    "Raspberry Pi 4 Model B": "https://www.robot-advance.com/userfiles/www.robot-advance.com/images/raspberry-4-modele-b-4go.jpg",
    "ESP32 Development Board": "https://probots.co.in/pub/media/catalog/product/cache/d8ddd0f9b0cd008b57085cd218b48832/e/s/esp32_wireless_bluetooth_38pin_development_board_with_cp2102_type-c_usb_interface_3_.jpg",
    "Compression Knee Sleeve": "https://cdn.shopify.com/s/files/1/0129/6942/products/cep-mid-knee-sleeve-black-4.webp?v=1680537612",
    "Tennis Racket Pro": "https://www.mistertennis.com/images/2024-media-01/head-speed-pro-310g-racchetta-da-tennis-236004_B.jpg",
    "Boxing Gloves 14oz": "https://academy.scene7.com/is/image/academy/21161434?%24pdp-thumbnails-xl-ng%24=",
    "Insulated Water Bottle 32oz": "https://bozbrand.com/products/boz-stainless-steel-water-bottle-vaccum-insulated-water-bottle-32-oz-green",
    "Resistance Band Kit": "https://armbet.net/products/exercise-resistance-bands",
    "Adjustable Dumbbell Set": "https://i5.walmartimages.com/seo/Renwick-4-90Lbs-Quick-Adjust-Dumbbell-Set-for-Home-Gym-Set-of-2-Black-Red_f37b1674-c1c0-4f66-9d87-2735838fef91.ca490a01096f38020186bda27648817f.jpeg?odnBg=FFFFFF&odnHeight=768&odnWidth=768",
    "Indoor Potted Succulent Set": "https://i5.walmartimages.com/seo/Succulent-Pots-3-6-Inch-4-Pack-Succulent-Planters-Small-Pots-Plants-Drainage-Tray-White-Ceramic-Flower-Planters-Indoor-Plants-Home-Office-Desk_9336bbf5-fa25-462d-825c-d016e41a33bf.9f3ddad6139da1e1d435e8d93143b756.jpeg",
    "Minimalist Wall Clock": "https://moiongeorge.nz/cdn/shop/files/karlsson-minimal-white-1-796px.png?v=1709869209",
    "Smart LED Bulb RGB": "https://media.falabella.com/falabellaCL/118175124_01/w%3D800%2Ch%3D800%2Cfit%3Dpad",
    "Genuine Leather Belt": "https://www.walmart.com/ip/Men-s-Belt-Genuine-Leather-Dress-Belts-for-Men-with-Single-Prong-Buckle-Classic-Fashion-Design-for-Work-Business-and-Casual-Brown-34in/836247086",
    "Knitted Winter Beanie": "https://eu-images.contentstack.com/v3/assets/blt7dcd2cfbc90d45de/blte3a3d84e2cd54941/60dc1769bcc58b0f8f8a8922/31-32c633a4350add50b1a30aa0bc1fced28.jpg",
    "Suede Chelsea Boots": "https://andresboots.com/products/a1003-statement-tansuede",
    "Minimalist Leather Wallet": "https://cdn01.pinkoi.com/product/PkdBfDjf/1/640x530.jpg",
    "Web Camera 1080p": "https://down-my.img.susercontent.com/file/my-11134207-820l4-mqrfyd70jy8b0d",
    "Ceramic Dinner Set 16pc": "https://images.thdstatic.com/productImages/91af44b1-321a-4ff2-83b5-b64a33f3a452/svn/black-16-pc-set-quickway-imports-dinnerware-sets-qi004501-64_600.jpg",
    "Yoga Mat Premium": "https://cdn.imweb.me/thumbnail/20220725/707f482173611.png",
    "Running Shoes Flex": "https://www.nike.com/t/flex-experience-run-12-mens-road-running-shoes-lqThC9",
    "Classic Denim Jacket": "https://www.gap.com/browse/product.do?pid=819666002&vid=2",
    "Scented Candle Trio": "https://www.saksfifthavenue.com/product/maison-francis-kurkdjian-scented-candle-trio-0400025510168.html"
}

def get_actual_image_url(url):
    if url.endswith(('.jpg', '.png', '.jpeg', '.webp')) or '1280' in url or 'images.unsplash.com' in url or 'image.coolblue.be' in url or 'images-na.ssl-images-amazon' in url or 'jpg' in url or 'png' in url or 'jpeg' in url or 'webp' in url:
        return url
    
    # Try to extract og:image from product pages
    try:
        res = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        og_img = soup.find('meta', property='og:image')
        if og_img and og_img.get('content'):
            img = og_img['content']
            if img.startswith('//'):
                img = 'https:' + img
            elif img.startswith('/'):
                img = 'https://' + url.split('/')[2] + img
            return img
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
    return url

for name, url in product_mapping.items():
    try:
        p = Product.objects.get(name=name)
        img_url = get_actual_image_url(url)
        
        print(f"Downloading {name} from {img_url}")
        res = requests.get(img_url, headers=HEADERS, timeout=10, verify=False)
        res.raise_for_status()
        
        jpg_path = os.path.join(products_dir, f"{p.slug}.jpg")
        with open(jpg_path, 'wb') as f:
            f.write(res.content)
            
        p.image.name = f"products/{p.slug}.jpg"
        p.save()
        print(f"Successfully updated {name}")
    except Product.DoesNotExist:
        print(f"Product {name} not found in DB")
    except Exception as e:
        print(f"Failed to download/update {name}: {e}")
        
print("All done!")
