import logging
import time 
import requests

from bs4 import BeautifulSoup as bs
from .shop_parser import ShopParser
from .item import Item 
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


class AliexpressParser(ShopParser):

    def __init__(self):
        ShopParser.__init__(self, "www.aliexpress.ru")


    def load_page(
        self,
        url: str, # Shop url
        ) -> bs:
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(url=url)
        time.sleep(5)
        html = driver.page_source
        soup = bs(html, "html.parser")
        return soup


    def parse_page(
        self,
        url: str,
        count: int,
        ):
        soup = self.load_page(url)
        container = soup.find_all("div", attrs=
        {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__horizontal__tusfnx product-snippet_ProductSnippet__imageSizeS__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
        if len(container) == 0:
            container = soup.find_all("div", attrs=
                {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__vertical__tusfnx product-snippet_ProductSnippet__imageSizeM__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
            
        result = []
        for block in container:
            if len(result) == count:
                break
            item = self.parse_block(block=block)
            if item.brand_name is None:
                continue
            result.append(item)
        return result

    
    def parse_block(
        self,
        block,
        ):
        

        url_block = block.find('a', class_='product-snippet_ProductSnippet__galleryBlock__tusfnx')
        if not url_block:
            return
        
        url = url_block.get('href')
        if not url:
            return 
        url = "https://aliexpress.ru" + url 

        brand_name_block = block.find('div', class_='product-snippet_ProductSnippet__caption__tusfnx')
        if not brand_name_block:
            return 
        
        brand_name = brand_name_block.text.strip()

        goods_name_block = block.find('div', class_='product-snippet_ProductSnippet__name__tusfnx')
        if not goods_name_block:
            return 
        
        goods_name = goods_name_block.text.strip()

        price_block = block.find('div', class_="snow-price_SnowPrice__mainM__1ehyuw")
        if not price_block:
            return 
        price = float(price_block.text
            .strip()
            .replace("\xa0","")
            .replace(" руб.","")
            .replace(",",""))

        image_block = block.find("img", class_="gallery_Gallery__image__1ln22f")
        if not image_block:
            return 
        image = image_block.attrs.get("src")
        if image:
            image = "https:" + image
        

        
        return Item(
            shop_name=self.shop_name,
            brand_name=brand_name,
            goods_name=goods_name,
            price=price,
            url=url,
            image=image,
        )
        