
class Item:

    def __init__(
        self,
        brand_name: str,
        goods_name: str,
        price: float,
        url: str,
        image: str,
        ):
        self.brand_name = brand_name
        self.goods_name = goods_name
        self.price = price 
        self.url = url 
        self.image = image 
    
    def __str__(self,):
        return f"Product:\n"\
               f"brand_name: {self.brand_name}\n"\
               f"goods_name: {self.goods_name}\n"\
               f"price: {self.price}\n"\
               f"url: {self.url}\n"