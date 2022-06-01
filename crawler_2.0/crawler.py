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

def get_products(category, feature, products_url):
    res = get_urls(products_url)
    soup = BeautifulSoup(res, 'html.parser')
    products = soup.find_all("div", attrs={'class': 'main_con js-product-block'})

    for product in products:
        product_url = product.find('a')['href']
        get_product(category, feature, product_url)

    print("get_products-Done")

    page = soup.find("span", attrs={'class': 'number'})
    next_page = soup.find_all("a", attrs={'class': 'number_line_a'})

    if page == None:
        return False

    for i in next_page:
        if i.string.isnumeric():
            if int(i.string) == int(page.string) + 1:
                return True
    return False


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


def get_product(category, feature, product_url):
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
        'main_image': main_image,
        'feature': feature
    }

    print(id)
    insert_product(product)
    insert_product_images(id, images)
    insert_product_variants(id, sizes)
    return "get_product-Done"

if __name__ == '__main__':
    category = 'men'
    features = {'短T': '1769', '長T': '1906', '印花短T': '38', '大學T/連帽T': '1943', 'POLO衫': '39', '背心': '40', '商務襯衫': '1885', '休閒襯衫': '1886', '針織衫/毛衣': '656',
             '休閒外套': '1917', '防風外套': '1916', '大衣/西裝': '1918', '短褲': '43', '牛仔褲': '1710', '西裝褲': '1712', '束口褲': '1874', '休閒褲': '1711', '帽子': '1456',
             '包包/皮夾': '1252', '皮帶': '2038', '男鞋': '1255', '太陽眼鏡': '2089'}

    for feature, code in features.items():
        page = 1
        while(True):
            products_url = f"https://www.net-fashion.net/category/{code}/{page}"
            next = get_products(category, feature, products_url)

            if next:
                page += 1
            else:
                page = 1
                break


    category = 'women'
    features = {'基本短T': '1781', '基本長T': '1930', '印花短T': '1670', '印花長T': '1932', '大學T/連帽T': '1931', 'POLO衫': '526', '設計上衣': '561', '基本背心': '1783', '設計背心': '22',
                '商務襯衫': '1882', '休閒襯衫': '1881', '設計襯衫': '1888', '針織衫/毛衣': '1936', '休閒外套': '1922', '防風外套': '1926', '抗UV外套': '1924', '西裝/大衣': '1923', '裙裝': '305',
                '短褲': '26', '牛仔褲': '1784', '西裝褲': '1907', '長褲': '25', '內搭褲': '1653', '洋裝/連身褲': '23', '肩背包': '1248', '後背包': '1249', '托特包': '1873', '皮夾': '1250',
                '帽子': '1237', '女鞋': '1492', '皮帶': '2061', '太陽眼鏡': '2088', '飾品': '2095'}

    for feature, code in features.items():
        page = 1
        while(True):
            products_url = f"https://www.net-fashion.net/category/{code}/{page}"
            next = get_products(category, feature, products_url)

            if next:
                page += 1
            else:
                page = 1
                break

    print("Done")