import requests
import shutil

url = "https://tse1.mm.bing.net/th/id/OIP.TsJoK7vxQTbb7PZvVWmeowHaFj?r=0&pid=Api&h=220&P=0"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, verify=False)
if r.status_code == 200:
    with open('test_bing_image.jpg', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        print("Downloaded")
