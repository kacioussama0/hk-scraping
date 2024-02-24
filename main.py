import requests
from bs4 import BeautifulSoup
import json
from datetime import date


URL = "https://app.hkpartners.online/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

session = requests.session()

response = session.get(URL + 'login')

soup = BeautifulSoup(response.content, "html.parser")

csrf_token = soup.find('input', attrs={'type': 'hidden'})['value'].strip()

CREDENTIALS = {
    "email": "mus.ibrahim.mus1998@gmail.com",
    "password": "Mustira1998",
    "login": "",
    "_token": csrf_token
}

r = session.post(URL + 'login', data=CREDENTIALS, cookies=session.cookies, headers={'User-Agent': USER_AGENT})

def get_categories():

    response = session.get(URL + 'marketer/products')
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('select', attrs={'name': 'category_id'}).find_all('option')

    return [{"id": category['value'] , "title": category.text} for category in categories][1:]


def get_products():


    response = session.get(URL + 'marketer/products')
    
    
    if response.ok:
            
        products = product_info(response)

        for category in get_categories():
                
            filter_response = session.get(URL + 'marketer/products?category_id=' + category['id'])
        
            for product in products:

                if product in product_info(filter_response):
                    product["category_id"] = category['id']
                    
            
                    

        return products



def get_products_json():
  
    data = get_products()
  
    if data: 
    
        today = date.today().strftime('%d-%m-%Y')

        newProducts = []

        for product in data:
             
             if "category_id" not in product:
                
                product["category_id"] = "null"
                
             newProducts.append(product | get_product(product['product_id']))

        data_json = {
           'title': 'Market 12 Products',
           'today': today,
           'products': newProducts
        }

        file_name = today + '-products.json'

        with open(file_name,'w') as file:

            json.dump(data_json,file,ensure_ascii=False)
            file.close()

def product_info(response):
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', id='products-list')

        if div != None:
            products = div.find_all('div', class_='product')
            orders_id = [product['data-id'] for product in products]
            products_image = [product.find('img')['src'] for product in products]
            products_title = [product.find('h2').text.strip() for product in products]
            products_qte = [int(product.find('div',style=" z-index: 2; ")['data-qty']) for  product in products]
            products_price = [int(product.find('h2',title="سعر المنتج").text.strip().replace('DA','').replace(',','')) for product in products]
            products_id = [product.find('a')['href'].replace(URL+'product/','').replace('/ref/5789','') for product in products]
            zipped = zip(orders_id,products_id,products_title,products_qte,products_price,products_image)    
            return [{'order_id': product[0],'product_id':  product[1],'title': product[2],'qte': product[3],'price': product[4],'image': product[5]} for product in zipped]

        else:
             return 404

        
def get_product(id):  
      
    response = session.get(URL + 'product/' + id + '/ref/5789')

    if response.ok:

        content = BeautifulSoup(response.content,'html.parser')
        order_box = content.find('div',attrs={'class': 'order-product-box'})
        description = order_box.find('section',id='product-description')
        title = order_box.find("div",attrs={"class": "title-section"}).find('span').text
        price = order_box.find("div",attrs={"class": "price-section"}).find("div",id="product-price").text.replace(" د.ج","");
        variantes = {}

        if(description != None): description = "".join([str(item) for item in description.contents])
        
        variantesBox = order_box.find('div',attrs={'class': 'variants-section'})

        variantesTitle = variantesBox.find('h2')

        if variantesTitle != None:

            if variantesTitle.text != '':

                productVariantes = variantesBox.findAll("div",attrs={'class': "product-variant"})   

                variantes = {
                    "title": variantesTitle.string,
                    "choices": [{"id": choice.find("input")['value'],  "name": choice.find("label").find("div").find("div").text } for choice in productVariantes],
                    "images": [image['data-img'] for image in productVariantes]
                }       
               
        return {
            "title": title,
            "description": description,
            "variantes": variantes,
            "price": int(price)
        }

       
    else:
        return False  
        
def get_categories_json():

    data = get_categories()
    today = date.today().strftime('%d-%m-%Y')
    file_name = today + '-categories.json'
    data_json = {
           'title': 'Market 12 Categories',
           'today': today,
           'categories': data
        }
    with open(file_name,'w') as file:
        json.dump(data_json,file,ensure_ascii=False)
        file.close()

# get_categories_json()
get_products_json()

