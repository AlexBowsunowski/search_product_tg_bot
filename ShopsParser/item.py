from PIL import Image 

class Item:

    def __init__(
        self,
        brand_name: str,
        goods_name: str,
        price: float,
        url: str,
        image: Image,
        ):
        self.brand_name = brand_name
        self.goods_name = goods_name
        self.price = price 
        self.url = url 
        self.image = image 
    
