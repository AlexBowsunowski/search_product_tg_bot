import os

TOKEN = os.environ['TELEGRAM_TOKEN']
#Число товаров которые будет выводить бот по умолчанию 
COUNT_SEARCH_ONE_SHOP = 5
COUNT_SEARCH_ALL_SHOP = 2
#Название кнопок, которые будем использовать
WILDBERRIES_BUTTON = "Найти товар на wildberries"
ALIEXPRESS_BUTTON = "Найти товар на aliexpress"
ALLSHOP_BUTTON = "Найти товар из всех предложенных магазинов"
SEARCH_EXIT_BUTTON = "Выйти из поиска"
SETTING_ONE_SHOP_BUTTON = "Сколько продуктов будем выводить при поиске в одном магазине"
SETTING_ALL_SHOP_BUTTON = "Сколько продуктов будем выводить при поиске по всем магазинам"
SETTING_LOOK_BUTTON = "Посмотреть текущие настройки"
SETTING_EXIT_BUTTON = "Выйти из настроек"


DB_NAME = "user.db"