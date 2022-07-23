import logging 

from shop_parser import ShopParser
from item import Item 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("wb")



class AliexpressParser(ShopParser):

    def __init__(self):
        ShopParser.__init__(self, "www.wildberries.ru")


    def parse_page(
        self,
        url: str,
        ):
        soup = self.load_page(url)
        container = soup.find_all("div", attrs=
        {'class': 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__vertical__tusfnx product-snippet_ProductSnippet__imageSizeM__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'})
        result = []
        for block in container:
            result.append(self.parse_block(block=block))
        return result

    
    def parse_block(
        self,
        block,
        ):
        

        url_block = block.find('a', class_='product-snippet_ProductSnippet__galleryBlock__tusfnx')
        if not url_block:
            logger.error('no url_block')
            return
        
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return 
        url = "https://aliexpress.ru" + url 

        brand_name_block = block.find('div', class_='product-snippet_ProductSnippet__caption__tusfnx')
        if not brand_name_block:
            logger.error("no brand name block")
            return 
        
        brand_name = brand_name_block.text.strip()

        goods_name_block = block.find('div', class_='product-snippet_ProductSnippet__name__tusfnx')
        if not goods_name_block:
            logger.error("no goods name block")
            return 
        
        goods_name = goods_name_block.text.strip()

        price_block = block.find('div', class_="snow-price_SnowPrice__mainM__1ehyuw")
        if not price_block:
            logger.error("no price block")
            return 
        price = float(price_block.text
            .strip()
            .replace("\xa0","")
            .replace(" руб.","")
            .replace(",",""))

        image_block = block.find("img", class_="gallery_Gallery__image__1ln22f")
        if not image_block:
            logger.error("no image block")
            return 
        image = image_block.attrs.get("src")
        if image:
            image = "https:" + image
        


        logger.info(f"{brand_name} \n {goods_name} \n {price} \n {url} \n {image} \n")

        logger.debug("="*200)
        return Item(
            brand_name=brand_name,
            goods_name=goods_name,
            price=price,
            url=url,
            image=image,
        )


    def run(
        self,
        url: str,
        ):
        result = self.parse_page(url)
        return result
        


if __name__ == '__main__':
    parser_shop = AliexpressParser()

    parser_shop.run(
        "https://aliexpress.ru/wholesale?catId=&SearchText=xiaomi%20mi%20band%207")

