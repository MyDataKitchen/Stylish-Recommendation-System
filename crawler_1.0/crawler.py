import requests
import random
import itertools
from bs4 import BeautifulSoup
from product_model import *

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

def get_urls(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None

def get_products(category, products_url):
    res = get_urls(products_url)
    soup = BeautifulSoup(res, 'html.parser')
    products = soup.find_all("div", attrs={'class': 'main_con js-product-block'})

    for product in products:
        product_url = product.find('a')['href']
        get_product(category, product_url)
    print("get_products-Done")


def insert_product_variants(id, product_sizes):
    colors = [1, 2, 3, 4, 5, 6, 7]
    stocks = [0, 1, 3, 4, 6, 8, 10, 12, 13, 16, 15, 20]
    sizes = []
    for size in product_sizes:
        try:
            size = size.find("div").string
            sizes.append(size)
        except:
            pass

    color = random.choices(colors, weights=(30, 40, 50, 60, 70, 80, 90), k=7)
    color_selected = list(dict.fromkeys(color))
    combinations = list(itertools.product(color_selected, sizes))

    for combination in combinations:
        stock = random.choices(stocks, weights=(70, 20, 30, 30, 70, 80, 90, 30, 40, 40, 50, 50), k=1)[0]
        variant = {
            "product_id": int(id),
            "color_id": combination[0],
            "size": combination[1],
            "stock": stock
        }
        insert_variant(variant)
    print("insert_product_variants-Done")
    return "insert_product_variants-Done"


def insert_product_images(id, images):
    for image in images:
        image = {
            'product_id': int(id),
            'image': image.find('img')['src']
        }
        insert_image(image)
    print("insert_product_images-Done")
    return "insert_product_images-Done"


def get_product(category, product_url):
    res = get_urls(product_url)
    soup = BeautifulSoup(res, 'html.parser')

    sizes = soup.find("div", attrs={'id': '[SPEC_NAME]'})
    images = soup.find("div", attrs={'class': 'html_block_detail'}).find_all("p", attrs={'align': 'center'})

    id = product_url.split('product/')[1]
    title = soup.find("div", attrs={'class': 'product_detail_Right_title'}).string.strip()
    price = soup.find("div", attrs={'class': 'product_priceR_real'}).b.string
    try:
        place = soup.find("div", attrs={'class': 'html_block_detail'}).find_all("p", attrs={'align': 'left'})[0].find('span').string.split(' ')[1]
    except:
        place = "中國製"

    try:
        texture = soup.find("div", attrs={'class': 'html_block_detail'}).find_all("p", attrs={'align': 'left'})[1].find('span').string.split('●')[1]
    except:
        texture = "商品材質 60%棉、40%聚酯纖維"

    try:
        wash = soup.find("div", attrs={'class': 'html_block_detail'}).find_all("p", attrs={'align': 'left'})[2].find('span').string.split('※')[1]
    except:
        wash = "建議放入洗衣袋中清洗，深淺色需分開，以避免染色問題。"

    main_image = soup.find("img", attrs={'id': 'PRODUCT_IMAGE_MAIN'})['src']

    product = {
        'id': int(id),
        'category': category,
        'title': title,
        'description': "厚薄:薄 彈性:無",
        'price': price,
        'place': place,
        'texture': texture,
        'wash': wash,
        'note': "實品顏色依單品照為主",
        'story': "O.N.S is all about options, which is why we took our staple polo shirt and upgraded it with slubby linen jersey, making it even lighter for those who prefer their summer style extra-breezy.",
        'main_image': main_image
    }

    print(id)
    insert_product(product)
    insert_product_images(id, images)
    insert_product_variants(id, sizes)
    return "get_product-Done"

if __name__ == '__main__':
    categorys = {'men': '1467', 'women': '1466'}
    for category, code in categorys.items():
        for page in range(1, 26):
            products_url = f"https://www.net-fashion.net/category/{code}/{page}"
            get_products(category, products_url)

    for page in range(1, 8):
        products_url = f"https://www.net-fashion.net/category/1551/{page}"
        get_products("accessories", products_url)

    for page in range(1, 4):
        products_url = f"https://www.net-fashion.net/category/2061/{page}"
        get_products("accessories", products_url)

    for page in range(1, 5):
        products_url = f"https://www.net-fashion.net/category/2095/{page}"
        get_products("accessories", products_url)

    for page in range(1, 4):
        products_url = f"https://www.net-fashion.net/category/1492/{page}"
        get_products("accessories", products_url)


    print("Done")