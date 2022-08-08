from dataclasses import dataclass


@dataclass
class Item:

    shop_name: str
    brand_name: str
    goods_name: str
    price: float
    url: str
    image: str

    def tlg_repr(self,) -> str:
        return f"Продукт:\n"\
               f"Название магазина: {self.shop_name}\n"\
               f"Название производителя: {self.brand_name}\n"\
               f"Название товара: {self.goods_name}\n"\
               f"Цена: {self.price} руб.\n"\
               f"Ссылка на товар: {self.url}\n"

    def __eq__(self, other: 'Item'):
        if self.shop_name != other.shop_name:
            return False
        elif self.brand_name != other.brand_name:
            return False
        elif self.goods_name != other.goods_name:
            return False
        elif self.price != other.price:
            return False
        elif self.url != other.url:
            return False
        elif self.image != other.image:
            return False
        return True
