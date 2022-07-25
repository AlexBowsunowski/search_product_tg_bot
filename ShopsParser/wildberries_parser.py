import logging 
import time 
import requests

from bs4 import BeautifulSoup as bs
from .shop_parser import ShopParser
from .item import Item 


logger = logging.getLogger("wb")



class WildberriesParser(ShopParser):

    def __init__(self):
        ShopParser.__init__(self, "www.wildberries.ru")

    
    def load_page(
        self,
        url: str, # Shop url
        page: int = None, # Shop page
        ):
        result = self.driver.get(url=url)
        time.sleep(5)
        html = self.driver.page_source
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
            if item.brand_name is None:
                continue
            result.append(item)
        return result

    
    def parse_block(
        self,
        block,
        ):
        

        url_block = block.find('a', class_='product-card__main j-card-link')
        if not url_block:
            logger.error('no url_block')
            return
        
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return 

        brand_name_block = block.find('strong', class_='brand-name')
        if not brand_name_block:
            logger.error("no brand name block")
            return 
        
        brand_name = brand_name_block.text.replace('/', '').strip()

        goods_name_block = block.find('span', class_='goods-name')
        if not goods_name_block:
            logger.error("no goods name block")
            return 
        
        goods_name = goods_name_block.text.strip()

        price_block = block.find('ins', class_="lower-price")
        if not price_block:
            logger.error("no price block")
            return 
        price = float(price_block.text
            .strip()
            .replace("\xa0","")
            .replace("₽",""))

        image_block = block.find("img", class_="j-thumbnail thumbnail")
        if not image_block:
            logger.error("no image block")
            return 
        image = "https:" + image_block.attrs.get("src")

        logger.info(f"{brand_name} \n {goods_name} \n {price} \n {url} \n {image} \n")

        logger.debug("="*200)
        return Item(
            brand_name=brand_name,
            goods_name=goods_name,
            price=price,
            url=url,
            image=image,
        )
