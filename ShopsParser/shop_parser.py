from abc import abstractmethod
from typing import List


class ShopParser:

    def __init__(
        self,
        shop_name: str, # Name of shop
        ):
        self.shop_name = shop_name
        

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