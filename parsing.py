
import requests
from bs4 import BeautifulSoup as bs

url = 'https://sokolushka.ru/magazin-lekarstvennyh-trav/folder/produkty-pchelovodstva'

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def parse(url, headers):
    pars_res = []
    session = requests.Session()
    request = session.get(url, headers = headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('form', attrs={'class': 'shop2-product-item product-item-thumb'})
        for div in divs:
            title = div.find('div', attrs={'class': 'product-name'}).text   #Название товара
            div_href = div.find('div', attrs={'class': 'product-name'})     #Ссылка на товар
            href = div_href.find('a').get('href')
            div_price = div.find('div', attrs={'class': 'price-current'})   #Цена
            price = div_price.find('strong').text
            pars_res.append({'title': title,
                             'href': 'https://sokolushka.ru' + href,
                             'price': price})
        print(len(pars_res))
    else:
        print('error')


parse(url, headers)