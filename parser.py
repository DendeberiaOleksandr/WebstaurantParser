import re

import requests
from bs4 import BeautifulSoup

from product import Product


def get_pages_size(page_url):
    res = requests.get(page_url)
    soup = BeautifulSoup(res.content, 'html5lib')
    pagination = soup.find(class_='rc-pagination')
    if pagination is None:
        return 1
    pagination_items = pagination.find_all(class_='rc-pagination-item')
    last_pagination_item = pagination_items[len(pagination_items) - 1]
    return int(last_pagination_item.text)


def get_items_urls(page_url):
    urls = []
    res = requests.get(page_url)
    soup = BeautifulSoup(res.content, 'html5lib')
    items = soup.find_all(class_='ag-item')
    for item in items:
        item_link = item.find('a', class_='block')
        urls.append(item_link['href'])
    return urls


def get_product(product_page_url):
    res = requests.get(product_page_url)
    soup = BeautifulSoup(res.content, 'html5lib')

    product_name = soup.find('h1', class_='page-header').text

    imgs = soup.find_all('img')
    mainImage = None

    for img in imgs:
        if img.has_attr('id'):
            if img['id'] == 'mainImage':
                mainImage = img
                break

    product_img = 'None'

    if mainImage is not None:
        product_img = mainImage['src']

    product_subhead = soup.find('div', class_='product-subhead')

    product_number = 'None'

    if product_subhead is not None:
        spans = product_subhead.find_all('span')

        for span in spans:
            if span.has_attr('itemprop'):
                if span['itemprop'] == 'sku':
                    product_number = span.text

    product_price = 'None'
    price = soup.find('p', class_='price')
    if price is not None:
        product_price = re.sub(r'[^$.0-9]', '', price.text)

    return Product(product_name, product_price, product_number, product_page_url, product_img)
