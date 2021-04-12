import requests

from bs4 import BeautifulSoup

import csv

CSV = 'cards.csv'
HOST = 'https://klubki-v-korzinke.ru/'
URL = 'https://klubki-v-korzinke.ru/category/novinki/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-block block')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', 'name').get_text(strip=True),
                'product_link': HOST + item.find('div', 'name').find('a').get('href'),
                'price': item.find('div', 'product-price').get_text(strip=True),
                'product_features': item.find('div', 'product-features').get_text(strip=True),
                'product_availability': item.find('div', 'available').get_text(strip=True),
                'product_description': item.find('div', 'offers').get_text(strip=True),
                'product_img': HOST + item.find('div', 'image').find('img').get('src')
            }
        )
    return cards


def save_doc(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование', 'Сссылка', 'Цена', 'Состав', 'Наличие на складе', 'Описание пряжи', 'Изображение пряжи'])
        for item in items:
            writer.writerow([item['title'], item['product_link'], item['price'], item['product_features'], item['product_availability'], item['product_description'], item['product_img']])


def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')


parser()
