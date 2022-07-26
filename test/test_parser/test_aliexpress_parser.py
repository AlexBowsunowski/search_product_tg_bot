import pytest 

from ShopsParser.aliexpress_parser import AliexpressParser

url_aliexpress = "https://aliexpress.ru/wholesale?SearchText={product}&g=undefined&page={page}"


# Проверим загрузку самой страницы(должен выводить не пустой текст)
def test_load_page():
    product1, page1 = "айфон+13", 1
    product2, page2 = "honor", 1

    url1 = url_aliexpress.format(product=product1, page=page1)
    url2 = url_aliexpress.format(product=product2, page=page2)

    ali_parser = AliexpressParser()
    soup_html1 = ali_parser.load_page(url1)
    soup_html2 = ali_parser.load_page(url2)
    assert len(soup_html1) != 0
    assert len(soup_html2) != 0

    container1 = soup_html1.find_all("div", attrs=
            {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__horizontal__tusfnx product-snippet_ProductSnippet__imageSizeS__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
    if len(container1) == 0:
        container1 = soup_html1.find_all("div", attrs=
            {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__vertical__tusfnx product-snippet_ProductSnippet__imageSizeM__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
    
    container2 = soup_html2.find_all("div", attrs=
            {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__horizontal__tusfnx product-snippet_ProductSnippet__imageSizeS__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
    if len(container2) == 0:
        container2 = soup_html2.find_all("div", attrs=
            {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__vertical__tusfnx product-snippet_ProductSnippet__imageSizeM__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
    

    assert len(container1) > 10
    assert len(container2) > 10


def test_parse_page():
    product1, page1 = "айфон+13", 1
    product2, page2 = "honor", 1

    url1 = url_aliexpress.format(product=product1, page=page1)
    url2 = url_aliexpress.format(product=product2, page=page2)

    ali_parser = AliexpressParser()
    items1 = ali_parser.parse_page(url1, 5)
    items2 = ali_parser.parse_page(url2, 5)
    assert len(items1) == 5
    assert len(items2) == 5