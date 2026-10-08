import urllib.request
import json

req = urllib.request.Request('http://localhost:8010/api/products/')
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    
    if isinstance(data, dict) and 'results' in data:
        items = data['results']
    elif isinstance(data, dict) and 'products' in data:
        items = data['products']
    else:
        items = data

    for item in items:
        if isinstance(item, dict):
            name = item.get('name')
            if name in ["Vintage Aviator Sunglasses", "Cotton Crewneck T-Shirt", "Slim Fit Chino Pants", "Canvas Tote Bag"]:
                print(f"{name}: {item.get('image')}")
