import os

file_path = 'frontend/src/pages/HomePage.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('name: "Clothing",', 'name: "Fashion",')
content = content.replace('link: "/products?category=Clothing",', 'link: "/products?category=Fashion",')

content = content.replace('name: "Home & Garden",', 'name: "Home",')
content = content.replace('link: "/products?category=Home%20%26%20Garden",', 'link: "/products?category=Home",')

content = content.replace('name: "Sports",', 'name: "Gaming",')
content = content.replace('link: "/products?category=Sports",', 'link: "/products?category=Gaming",')
content = content.replace('https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=2070&auto=format&fit=crop', 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
