from abc import abstractmethod
from typing import List

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


class ShopParser:

    def __init__(
        self,
        shop_name: str, # Name of shop
        ):
        self.shop_name = shop_name
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    @abstractmethod
    def load_page(
        self,
        url: str, # Shop url
        page: int = None, # Shop page
        ):
        pass
   

    @abstractmethod
    def parse_page(
        self,
        url: str,
        count: int,
        ):
        pass 


    @abstractmethod
    def parse_block(
        self,
        block,
        ):
        pass 


    def run(
        self,
        start_url: str,
        product: str,
        page: int=1,
        count: int=10,
        ) -> List:
        url = start_url.format(product=product, page=page)
        result = self.parse_page(url, count)
        return result