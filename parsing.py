import requests
from bs4 import BeautifulSoup as bs
import csv
import threading

# Все входные данные находятся здесь
url = 'https://sokolushka.ru/magazin-lekarstvennyh-trav/folder/produkty-pchelovodstva/p/0'

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

name = input('Введите имя потока 1: ')
name2 = input('Введите имя потока 2: ')

# Функция парсинга сайта СОКОЛУШКА
def parse(url, headers, name):
    print('Поток {} запущен'.format(name))
    urls = []
    urls.append(url)
    pars_res = []
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('li', attrs={'class': 'page-num'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://sokolushka.ru/magazin-lekarstvennyh-trav/folder/produkty-pchelovodstva/p/{i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('form', attrs={'class': 'shop2-product-item product-item-thumb'})
            for div in divs:
                try:
                    title = div.find('div', attrs={'class': 'product-name'}).text  # Название товара
                    div_href = div.find('div', attrs={'class': 'product-name'})  # Ссылка на товар
                    href = div_href.find('a').get('href')
                    div_price = div.find('div', attrs={'class': 'price-current'})  # Цена
                    price = div_price.find('strong').text
                    pars_res.append({'title': title,
                                     'href': 'https://sokolushka.ru' + href,
                                     'price': price})
                except:
                    pass
            print(len(pars_res))
    else:
        print('Поток {} - ERROR'.format(name))
    print('Поток {} Отработан. Переходим к созданию файла'.format(name))
    file_writer(pars_res, name)

# Функция выгрузки парсинга в csv-файл
def file_writer(pars_res, name):
    with open('sokolushka_honey{}.csv'.format(name), 'w', newline='') as f:
        pen = csv.writer(f)
        pen.writerow(('Наименование', 'Ссылка', 'Цена'))
        for i in pars_res:
            pen.writerow((i['title'], i['href'], i['price']))
    print('Файл sokolushka_honey{} создан'.format(name))


t = threading.Thread(target=parse, name='{}'.format(name), args=(url, headers, name))
t2 = threading.Thread(target=parse, name='{}'.format(name2), args=(url, headers, name2))
t.start()
t2.start()

# results = parse(url, headers, name)
# file_writer(results, name)
