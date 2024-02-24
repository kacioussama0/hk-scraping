import requests
from bs4 import BeautifulSoup

URL = "https://app.hkpartners.online/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

session = requests.session()

response = session.get(URL + 'product/GIsBFx/ref/5789')

soup = BeautifulSoup(response.content, "html.parser")

csrf_token = soup.find('input', attrs={'type': 'hidden'})['value'].strip()

print(csrf_token)

payload = {
    "_token": csrf_token,
    "name": "test ssss",
    "phone": "0232311222",
    "source": "https://app.hkpartners.online/product/GIsBFx",
    "state": 22,
    "city":"Algeria" ,
    "delivery_type": 2,
    "add_associated_product_too": 0,
    #"variant": 133,
    "quantity": 4,
    "referrer": 5789
}

order = requests.post(URL + "product/118/order",data=payload,cookies=session.cookies,headers={'User-Agent': USER_AGENT})

soup_response = BeautifulSoup(order.content,"html.parser")

print(soup_response.prettify())
