import logging 
import time 

from bs4 import BeautifulSoup as bs
from .shop_parser import ShopParser
from .item import Item 
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

class WildberriesParser(ShopParser):

    def __init__(self):
        ShopParser.__init__(self, "www.wildberries.ru")

    
    def load_page(
        self,
        url: str, # Shop url
        ):
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
        container = soup.find_all("div", attrs={'class': 'product-card j-card-item j-good-for-listing-event'})
        result = []
        for block in container:
            if len(result) == count:
                break
            item = self.parse_block(block=block)
            if item is None or item.brand_name is None:
                continue
            result.append(item)
        return result

    
    def parse_block(
        self,
        block,
        ):
        

        url_block = block.find('a', class_='product-card__main j-card-link')
        if not url_block:
            return
        
        url = url_block.get('href')
        if not url:
            return 

        brand_name_block = block.find('strong', class_='brand-name')
        if not brand_name_block:
            return 
        
        brand_name = brand_name_block.text.replace('/', '').strip()

        goods_name_block = block.find('span', class_='goods-name')
        if not goods_name_block:
            return 
        
        goods_name = goods_name_block.text.strip()

        price_block = block.find('ins', class_="lower-price")
        if not price_block:
            return 
        price = float(price_block.text
            .strip()
            .replace("\xa0","")
            .replace("₽",""))

        image_block = block.find("img", class_="j-thumbnail thumbnail")
        if not image_block:
            return 
        image = "https:" + image_block.attrs.get("src")

        return Item(
            shop_name=self.shop_name,
            brand_name=brand_name,
            goods_name=goods_name,
            price=price,
            url=url,
            image=image,
        )
