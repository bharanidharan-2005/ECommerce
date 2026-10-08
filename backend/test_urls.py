import requests

images = {
    "Vintage Aviator Sunglasses": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80",
    "Cotton Crewneck T-Shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80",
    "Slim Fit Chino Pants": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80",
    "Canvas Tote Bag": "https://images.unsplash.com/photo-1597818449622-44670081d6d6?auto=format&fit=crop&w=800&q=80",
    "Winter Parka Coat": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?auto=format&fit=crop&w=800&q=80"
}

for name, url in images.items():
    res = requests.head(url)
    print(f"{name}: {res.status_code}")
