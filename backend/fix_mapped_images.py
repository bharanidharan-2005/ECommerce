import os
import django
import requests
from bs4 import BeautifulSoup
import time

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
    "Foam Roller": "https://cdn11.bigcommerce.com/s-faeolk0d25/images/stencil/1280x1280/products/160/651/208947ce-33a6-42e0-918b-4ae85c6556fa.0b422c7e08b55e1a4141476680560100__40352.1690544409.jpg",
    "Sneaker Cleaning Kit": "https://www.snkrehab.co.uk/cdn/shop/files/Image_1.png?v=1746558846&width=2000",
    "Jump Rope": "https://kronos-shop.pl/hpeciai/c5d2126e9145f9e58de56557062d8fa0/pol_pm_SPOKEY-Skakanka-Szybkosciowa-Do-Cwiczen-Fitness-Regulowana-Dlugosc-300-cm-18914_7.png",
    "Silver Hoop Earrings": "https://highsparksilver.com/cdn/shop/products/18MM-01_7.jpg?v=1771577455&width=416",
    "Gaming Mouse": "https://assets3.razerzone.com/LQ1cxhHVvbhiSLOMjv3r4MoTo4g=/1920x1280/https%3A%2F%2Fmedias-p1.phoenix.razer.com%2Fsys-master-phoenix-images-container%2Fh08%2Fh61%2F9765618188318%2Fviper-v3-pro-black-500x500.png",
    "Ceramic Plant Pot": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
    "Leather Belt": "https://levi.in/cdn/shop/files/877920001_2_Front_653c9280-e512-43f7-b4eb-cd1728a0cf07.jpg?v=1706682050",
    "Yoga Block Set": "https://i.ebayimg.com/images/g/oh8AAOSwSuplkvzi/s-l1200.png",
    "Bluetooth Tracker Tag": "https://f.nooncdn.com/p/pzsku/Z8A9BA053483E981C2F4DZ/45/1744406311/e9735dfd-34de-468b-852c-c699a8dbd7c2.jpg?width=1200",
    "Podcast Microphone": "https://image.coolblue.be/500x500/products/2045312",
    "Espresso Machine": "https://images-na.ssl-images-amazon.com/images/I/41e4ClleggL._SL500_._AC_SL500_.jpg",
    "Winter Parka Coat": "https://canadasportswear.com/cdn/shop/files/6100-GUNMETAL-FRONT_b756ba60-c95b-4bd5-b3f6-1dc4bef103ef_535x.png?v=1698767023",
    "Linen Bed Sheets": "https://crdms.images.consumerreports.org/f_auto%2Cw_1200/prod/products/cr/models/412835-natural-fabrics-quince-european-linen-10038228.png",
    "Resistance Band Set": "https://images.fyndiq.se/images/f_auto/t_600x600/prod/fdf2e18e548941b2/30bd544ac87b/5-pack-traningsband-gummiband-motstandsband-traningsband-multicolor-multifarg",
    "French Press Coffee Maker": "https://dualilacafe.com.br/cdn/shop/files/PRENSA_FRANCESA_WEBP_4c64a1d1-c9a4-4971-a563-8be176392eeb.webp?v=1763434669",
    "Wireless Charging Pad": "https://www.belkin.com/dw/image/v2/BGBH_PRD/on/demandware.static/-/Sites-master-product-catalog-blk/default/dw1c593379/images/hi-res/7/7d4364523d4952a0_WIZ019-BLK_MagSafe_BoostChargePro_2in1WirelessChargeDock_Hero_WEB.jpg?sfrm=png&sh=700&sm=fit&sw=700",
    "Graphic T-Shirt": "https://levi.in/cdn/shop/files/A79730246_01_Styleshot.jpg?v=1771917304",
    "Cast Iron Skillet": "https://www.lodgecastiron.com/products/chef-collection-3-piece-skillet-set",
    "Mechanical Pencil Set": "https://cdn.quick-backup.shop/cdn/1529/2025/01/06/thumb100-main-Nicpro-2-PCS-09-mm-Metal-Mechanical-Pencils-Set-Drafting-Pencil-for-Artist-Writing-Sketching-Drawing-with-4-Tubes-HB-Lead-Refill-ampamp-Erasers-Eraser-7388901-4735836.jpg",
    "Leather Wallet": "https://www.galenleather.com/cdn/shop/products/no48-personalized-handmade-leather-wallet-rustic-brown_300x.jpg?v=1606568177",
    "Smart Home Hub": "https://smartmatters.co/cdn/shop/products/smartthings-smart-home-hub-aeotec_a_1495x1495.jpg?v=1630595037",
    "Stainless Steel Water Bottle": "https://annamsshop.com/cdn/shop/files/IMG-1894.png?v=1777568127&width=1445",
    "Drone with 4K Camera": "https://toputra.com/products/azemov-drone-with-4k-camera",
    "Portable SSD 1TB": "https://auspost.com.au/shop/product/sandisk-portable-ssd-1tb-usb-3-2-10001614",
    "Fleece Throw Blanket": "https://www.desertcart.in/products/28596325-bedsuresherpa-fleece-throw-blanket-for-couch-thick-and-warm-blanket",
    "Gold Plated Necklace": "https://www.laceandfavour.com/wedding-necklaces/olivia-burton-amity-interlock-gold-plated-necklace/",
    "Leather Dress Shoes": "https://cdn.shopify.com/s/files/1/0830/7487/5738/files/20251110_1739_PremiumLeatherDressShoes_remix_01k9r24ewff5qajk9fxr6xmtk7.png?v=1773741349"
}

def get_actual_image_url(url):
    if url.endswith(('.jpg', '.png', '.jpeg', '.webp')) or 'images.unsplash.com' in url or 'image.coolblue.be' in url or 'images-na.ssl-images-amazon' in url:
        return url
    
    # Try to extract og:image from product pages
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
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
        res = requests.get(img_url, headers=HEADERS, timeout=10)
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
