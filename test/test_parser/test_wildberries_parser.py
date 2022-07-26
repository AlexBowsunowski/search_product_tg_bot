import pytest 

from ShopsParser.wildberries_parser import WildberriesParser

url_wildberries = "https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search={product}"


# Проверим загрузку самой страницы(должен выводить не пустой текст)
def test_load_page():
    product1, page1 = "айфон+13", 2
    product2, page2 = "honor", 3

    url1 = url_wildberries.format(product=product1, page=page1)
    url2 = url_wildberries.format(product=product2, page=page2)

    wild_parser = WildberriesParser()
    soup_html1 = wild_parser.load_page(url1)
    soup_html2 = wild_parser.load_page(url2)
    assert len(soup_html1) != 0
    assert len(soup_html2) != 0

    container1 = soup_html1.find_all("div", attrs={'class': 'product-card j-card-item j-good-for-listing-event'})
    container2 = soup_html2.find_all("div", attrs={'class': 'product-card j-card-item j-good-for-listing-event'})

    assert len(container1) == 20
    assert len(container2) == 20


def test_parse_page():
    product1, page1 = "айфон+13", 1
    product2, page2 = "honor", 1

    url1 = url_wildberries.format(product=product1, page=page1)
    url2 = url_wildberries.format(product=product2, page=page2)

    wild_parser = WildberriesParser()
    items1 = wild_parser.parse_page(url1, 5)
    items2 = wild_parser.parse_page(url2, 5)
    assert len(items1) == 5
    assert len(items2) == 5