import requests
import shutil

url = "https://cdn.mydukaan.io/app/image/357x357/?url=https://mydukaan.s3.amazonaws.com/4095334/aed5eba0-f960-4532-acdb-c318a2972346/1619149957779-920a1f31-4e04-476d-96e3-8076fa8a1d8a.jpeg"

response = requests.get(url, stream=True)
with open("img.png", "wb") as out_file:
    shutil.copyfileobj(response.raw, out_file)
