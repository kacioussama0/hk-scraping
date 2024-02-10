# import libraries
import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
import json

url = "https://app.hkpartners.online/"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

session = requests.session()

response = session.get(url + 'login')

soup = BeautifulSoup(response.content, "html.parser")
csrf_token = soup.find('input', attrs={'type': 'hidden'})['value'].strip()

credentials = {
    "email": "mus.ibrahim.mus1998@gmail.com",
    "password": "Mustira1998",
    "login": "",
    "_token": csrf_token
}

r = session.post(url + 'login', data=credentials, cookies=session.cookies, headers={'User-Agent': user_agent})


def get_products():

    response = session.get('https://app.hkpartners.online/marketer/products')

    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', id='products-list')

    products = div.find_all('div', class_='product')

    products_image = [product.find('img')['src'] for product in products]
    products_title = [product.find('h2').text.strip() for product in products]
    products_qte = [int(product.find('div',style=" z-index: 2; ")['data-qty']) for  product in products]
    products_price = [int(product.find('h2',title="سعر المنتج").text.strip().replace('DA','').replace(',','')) for product in products]

    return zip(products_title,products_qte,products_price,products_image)


def get_products_txt():
    table = tabulate(get_products(),['title','qte','price','image'],tablefmt='heavy_grid',showindex="always")
    print(table)
    with open("products.txt","w",encoding="utf-8") as file:
        file.write("HK Products\n")
        file.write(table)


get_products_txt()