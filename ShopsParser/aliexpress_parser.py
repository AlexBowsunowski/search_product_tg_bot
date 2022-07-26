import time 

from bs4 import BeautifulSoup as bs
from .shop_parser import ShopParser
from .item import Item 
from . import config as cfg
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
        time.sleep(1)
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
        {'class': cfg.ALI_NAME_BLOCK1})
        if len(container) == 0:
            container = soup.find_all("div", attrs=
                {'class': cfg.ALI_NAME_BLOCK2})
            
        result = []
        for block in container:
            if len(result) == count:
                break
            item = self.parse_block(block=block)
            if item is None:
                continue
            result.append(item)
        return result

    
    def parse_block(
        self,
        block,
        ):
        

        url_block = block.find('a', class_=cfg.ALI_NAME_URL)
        if not url_block:
            return
        
        url = url_block.get('href')
        if not url:
            return 
        url = "https://aliexpress.ru" + url 

        brand_name_block = block.find('div', class_=cfg.ALI_NAME_BRAND)
        if not brand_name_block:
            return 
        
        brand_name = brand_name_block.text.strip()

        goods_name_block = block.find('div', class_=cfg.ALI_NAME_GOODS)
        if not goods_name_block:
            return 
        
        goods_name = goods_name_block.text.strip()

        price_block = block.find('div', class_=cfg.ALI_NAME_PRICE)
        if not price_block:
            return 
        price = float(price_block.text
            .strip()
            .replace("\xa0","")
            .replace(" руб.","")
            .replace(",",""))

        image_block = block.find("img", class_=cfg.ALI_NAME_IMAGE)
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
        