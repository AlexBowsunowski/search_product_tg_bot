from abc import abstractmethod
from typing import List
from .item import Item

class ShopParser:
    """
    Класс шаблон для конкретного парсера маркетплейса
    """
    def __init__(
        self,
        shop_name: str, # Name of shop
        ):
        self.shop_name = shop_name
        

    @abstractmethod
    def load_page(
        self,
        url: str, # Shop url
        ):
        """
        Метод для загрузки страницы сайта. 
        Для каждого магазина он будет работать по своему. 
        Должен возвращать класс BeatifulSoup где загружена сама поисковая страничка сайта.
        """
        

    @abstractmethod
    def parse_page(
        self,
        url: str,
        count: int,
        ):
        """
        Загружаем страничку сайта через load_page.
        Далее загружаем список с блоками товара на каждой страничке.
        И циклом проходимся по каждому блоку товара(каждый блок парсим через parse_block)

        Args:
            url (str): страничка сайта
            count (int): число продуктов, которые надо выдать
            (Продукт должен быть не None, т.е. не должен содержать пропущенных значений)

        Returns:
            Список объектов класса Item
        """


    @abstractmethod
    def parse_block(
        self,
        block,
        ):
        """
        Для каждого блока находим следующую информацию:
            1. Ссылка на товар
            2. Название производителя
            3. Название товара
            4. Цена в руб.
            5. Ссылка на картинку с товаром

        Args:
            block (BeatifulSoup): блок, содержащий информацию о товаре 
        Returns:
            Объект класса Item
        """


    def run(
        self,
        start_url: str,
        product: str,
        page: int=1,
        count: int=10,
        ) -> List[Item]:
        """
        Форматируем start_url подставляя в строку название товара и номер страницы

        Args:
            start_url (str): ссылка-шаблон на сайт
            product (str): название продукта
            page (int, optional): номер страницы. Defaults to 1.
            count (int, optional): число товаров которые надо спарсить. Defaults to 10.

        Returns:
            List[Item]: список содержащий объекты класса Item
        """
        url = start_url.format(product=product, page=page)
        result = self.parse_page(url, count)
        return result