import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

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
   
        
