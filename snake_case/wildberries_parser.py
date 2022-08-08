import logging
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from . import config as cfg
from .item import Item
from .shop_parser import ShopParser


class WildberriesParser(ShopParser):

    def __init__(self):
        super().__init__("www.wildberries.ru", cfg.URL_WILDBERRIES)

    def load_page(
        self,
        url: str,  # Shop url
    ):
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=options)
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
        container = soup.find_all("div", attrs={'class': cfg.WILD_NAME_BLOCK})
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

        url_block = block.find('a', class_=cfg.WILD_NAME_URL)
        if not url_block:
            return

        url = url_block.get('href')
        if not url:
            return

        brand_name_block = block.find('strong', class_=cfg.WILD_NAME_BRAND)
        if not brand_name_block:
            return

        brand_name = brand_name_block.text.replace('/', '').strip()

        goods_name_block = block.find('span', class_=cfg.WILD_NAME_GOODS)
        if not goods_name_block:
            return

        goods_name = goods_name_block.text.strip()

        price_block = block.find('ins', class_=cfg.WILD_NAME_PRICE)
        if not price_block:
            return
        price = float(price_block.text
                      .strip()
                      .replace("\xa0", "")
                      .replace("₽", ""))

        image_block = block.find("img", class_=cfg.WILD_NAME_IMAGE)
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
