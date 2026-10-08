import sys
filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\HomePage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''  {
    name: "Gaming",
    image: "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=gaming",
    count: "90+ Items"
  },
  {
    name: "Audio",
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=audio",
    count: "45+ Items"
  },
  {
    name: "Smart Devices",
    image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=smart-devices",
    count: "60+ Items"
  }'''

replacement = '''  {
    name: "Fashion",
    image: "https://images.unsplash.com/photo-1445205170230-053b83016050?q=80&w=2071&auto=format&fit=crop",
    link: "/products?category=fashion",
    count: "90+ Items"
  },
  {
    name: "Accessories",
    image: "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=accessories",
    count: "45+ Items"
  },
  {
    name: "Home & Living",
    image: "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?q=80&w=2069&auto=format&fit=crop",
    link: "/products?category=home",
    count: "60+ Items"
  }'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated HomePage.jsx successfully.')
else:
    print('Target string not found.')
