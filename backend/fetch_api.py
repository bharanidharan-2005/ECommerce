import urllib.request
import json

req = urllib.request.Request('http://localhost:8010/api/products/')
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    
    for item in data:
        name = item.get('name')
        if name in ["Vintage Aviator Sunglasses", "Cotton Crewneck T-Shirt", "Slim Fit Chino Pants", "Canvas Tote Bag"]:
            print(f"{name}: {item.get('image')}")
