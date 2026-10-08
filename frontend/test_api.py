import sys
import requests

url = "http://localhost:8010/api/orders/admin/"

try:
    response = requests.get(url)
    print("Status:", response.status_code)
    # The API might need authentication, we'll get a 401 or 403, which is fine, it means the URL exists
except Exception as e:
    print(e)
