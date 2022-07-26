
class Item:

    def __init__(
        self,
        shop_name: str,
        brand_name: str,
        goods_name: str,
        price: float,
        url: str,
        image: str,
        ):
        self.shop_name = shop_name
        self.brand_name = brand_name
        self.goods_name = goods_name
        self.price = price 
        self.url = url 
        self.image = image 
    
    def __str__(self,):
        return f"Продукт:\n"\
               f"Название магазина: {self.shop_name}\n"\
               f"Название производителя: {self.brand_name}\n"\
               f"Название товара: {self.goods_name}\n"\
               f"Цена: {self.price} руб.\n"\
               f"Ссылка на товар: {self.url}\n"