#Скрипт прохождения по ссылкам, извлечение контента и выгрузка в файл csv


#импорт библиотек
#requests извлекает html-страницу, BS - для синтаксического разбора html/xml
#csv - для сохранения данных в csv-формате
#threading - для создания нескольких потоков
import requests
from bs4 import BeautifulSoup as bs
import csv
import threading

# ссылка на страницу с товарами
url = 'https://sokolushka.ru/magazin-lekarstvennyh-trav/folder/produkty-pchelovodstva/p/0'
# заголовок сайта (симулируем работу через браузер)
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
# два потока для выполнения скрипта
name = input('Введите имя потока 1: ')
name2 = input('Введите имя потока 2: ')

# Функция парсинга сайта СОКОЛУШКА
# на входе: ссылка, заголовок сайта, имя потока
def parse(url, headers, name):
    print('Поток {} запущен'.format(name))
    # создаем пустой список для наполнения ссылками сайта
    urls = []
    # первая ссылка всегда начинается с 1-й страницы. Добавляем ее в список
    urls.append(url)
    # пустой словарь, будут заноситься спарсенные данные
    pars_res = []
    # открываем сессию (иллюзия работы через браузер под юзером)
    session = requests.Session()
    # get-запрос на выходе принимает объект
    request = session.get(url, headers=headers)
    # код 200 = успешное соединение с сайтом
    if request.status_code == 200:
        # загрузка страницы с контентом
        soup = bs(request.content, 'lxml')
        # находим число страниц с товарами
        try:
            pagination = soup.find_all('li', attrs={'class': 'page-num'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://sokolushka.ru/magazin-lekarstvennyh-trav/folder/produkty-pchelovodstva/p/{i}'
                if url not in urls:
                    urls.append(url)
        # в случае отсутствия сайт будет содержать только 1 (текущую) страницу с товарами
        except:
            pass
        # обход списка ссылок на товары
        for url in urls:
            # от кажждой ссылки в списке получаем контент
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            # ищем в коде страницы все
            # теги form с классом shop2-product-item product-item-thumb
            divs = soup.find_all('form', attrs={'class': 'shop2-product-item product-item-thumb'})
            # обходим найденные div'ы
            for div in divs:
                # ищем внутри тега полезные данные
                try:
                    title = div.find('div', attrs={'class': 'product-name'}).text  # Название товара
                    div_href = div.find('div', attrs={'class': 'product-name'})  # Ссылка на товар
                    href = div_href.find('a').get('href')
                    div_price = div.find('div', attrs={'class': 'price-current'})  # Цена
                    price = div_price.find('strong').text
                    # вносим в словарь спарсенных данных
                    pars_res.append({'title': title,
                                     'href': 'https://sokolushka.ru' + href,
                                     'price': price})
                # в случае какой-либо ошибки пропустить эту запись
                except:
                    pass
            print(len(pars_res))
    #если отклика нет
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

# инициализация потоков и их запуск
t = threading.Thread(target=parse, name='{}'.format(name), args=(url, headers, name))
t2 = threading.Thread(target=parse, name='{}'.format(name2), args=(url, headers, name2))
t.start()
t2.start()

# results = parse(url, headers, name)
# file_writer(results, name)
