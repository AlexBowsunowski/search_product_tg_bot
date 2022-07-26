import telebot 
from typing import List
from telebot import types 
from search_bot import config as cfg
from search_bot import database as db
from search_bot import exception as e
from ShopsParser.wildberries_parser import WildberriesParser
from ShopsParser.aliexpress_parser import AliexpressParser

print(cfg.TOKEN)
bot = telebot.TeleBot(cfg.TOKEN)
user = db.User()


@bot.message_handler(commands=['start'])
def send_keyboard(
    message,
    text="Привет, я бот для поиска товаров в разных магазинах"
    ):
    bot.send_message(
        message.chat.id,
        text=text,
    )
    bot.send_message(
        message.chat.id,
        text="Мои команды: \n /search - команда для поиска товара \n /settings - настройки поиска"
    )


@bot.message_handler(commands=['settings'])
def settings_keyboard(
    message,
    text="Вы вошли в настройки по поиску товара"):
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    one_shop_button = types.KeyboardButton(cfg.SETTING_ONE_SHOP_BUTTON)
    all_shop_button = types.KeyboardButton(cfg.SETTING_ALL_SHOP_BUTTON)
    look_settings_button = types.KeyboardButton(cfg.SETTING_LOOK_BUTTON)
    exist_button = types.KeyboardButton(cfg.SETTING_EXIT_BUTTON)

    keyboard.add(one_shop_button)
    keyboard.add(all_shop_button)
    keyboard.add(look_settings_button)
    keyboard.add(exist_button)

    message = bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(message, settings_callback) 


def settings_callback(message):
    if message.text == cfg.SETTING_ONE_SHOP_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Введите число продуктов"
        )
        bot.register_next_step_handler(message, set_settings, cfg.SETTING_ONE_SHOP_BUTTON)
    elif message.text == cfg.SETTING_ALL_SHOP_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Введите число продуктов"
        )
        bot.register_next_step_handler(message, set_settings, cfg.SETTING_ALL_SHOP_BUTTON)
    elif message.text == cfg.SETTING_LOOK_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Ваши текущие настройки:"
        )
        get_settings(message)
    elif message.text == cfg.SETTING_EXIT_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Выходим из настроек"
        )


def set_settings(message, type_of_set):
    if type_of_set == cfg.SETTING_ONE_SHOP_BUTTON:
        user.set_count_one_shop(message=message)
        message = bot.send_message(
            message.chat.id,
            text="Настройки обновлены!"
        )
    elif type_of_set == cfg.SETTING_ALL_SHOP_BUTTON:
        user.set_count_all_shop(message=message)
        message = bot.send_message(
            message.chat.id,
            text="Настройки обновлены!"
        )
    settings_keyboard(
        message=message,
        text="Возвращаемся к настройкам"
    )


def get_settings(message):
    result = "Количество товаров при поиске по одному магазину: {count_one}\n" \
            "Количество товаров при поиске по всем магазинам: {count_all}"
    try:
        count_one = user.get_count_one_shop(message=message)
        count_all = user.get_count_all_shop(message=message)
    except e.CountNotExists:
        count_one = cfg.COUNT_SEARCH_ONE_SHOP
        count_all = cfg.COUNT_SEARCH_ALL_SHOP

    message = bot.send_message(
        message.chat.id,
        text=result.format(count_one=count_one, count_all=count_all)
    )
    settings_keyboard(
        message=message,
        text="Возвращаемся к настройкам"
    )


@bot.message_handler(commands=['search'])
def search_keyboard(message, text="Привет, чем я могу тебе помочь?"):
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    wildberries_button = types.KeyboardButton(cfg.WILDBERRIES_BUTTON)
    aliexpress_button = types.KeyboardButton(cfg.ALIEXPRESS_BUTTON)
    allshop_button = types.KeyboardButton(cfg.ALLSHOP_BUTTON)
    keyboard.add(wildberries_button)
    keyboard.add(aliexpress_button)
    keyboard.add(allshop_button)

    message = bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    bot.register_next_step_handler(message, callback)    


def callback(message):
    if message.text == cfg.WILDBERRIES_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.WILDBERRIES_BUTTON)
    elif message.text == cfg.ALIEXPRESS_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.ALIEXPRESS_BUTTON)
    elif message.text == cfg.ALLSHOP_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.ALLSHOP_BUTTON)

#TODO: Попробовать отчистить по максимуму от if else
def search(message, shop):
    results = []
    bot.send_message(
        chat_id=message.chat.id,
        text="Ищу...",
    )
    if shop == cfg.ALLSHOP_BUTTON:
        count = count_parsing(message, True)
    else:
        count = count_parsing(message)
    product = message.text.strip().replace(" ", "%20")
    if shop == cfg.WILDBERRIES_BUTTON or shop == cfg.ALLSHOP_BUTTON:
        parser_shop = WildberriesParser()
        result = get_products(parser_shop=parser_shop, url=cfg.URL_WILDBERRIES, name_product=product, count_product=count) 
        results.extend(result)
    if shop == cfg.ALIEXPRESS_BUTTON or shop == cfg.ALLSHOP_BUTTON:
        parser_shop = AliexpressParser()
        result = get_products(parser_shop=parser_shop, url=cfg.URL_ALIEXPRESS, name_product=product, count_product=count) 
        results.extend(result)
    
    send_products(message=message, products=results)

    search_keyboard(
        message=message,
        text="Чем еще могу помочь?"
    )


def get_products(
    parser_shop: AliexpressParser | WildberriesParser,
    url: str,
    name_product: str,
    count_product: int) -> List:
    page = 1
    total = 0
    result = []
    while count_product != total: #TODO: Учесть момент, когда количество товаров может меньше запрошенного пользователем(Вывести меньше просто)
        print(f"url:{url}\npage:{page}\ntotal:{total}")
        products = parser_shop.run(url, name_product, page=page, count=count_product - total)
        total += len(products)
        result.extend(products)
        page += 1
    return result
    


def send_products(message, products):
    for product in products:
        bot.send_message(
            chat_id=message.chat.id,
            text=str(product)
        )
        bot.send_photo(
            message.chat.id,
            product.image,
        )


def count_parsing(message, all_shop=False) -> int:
    count = 0
    try:
        if all_shop:
            count = user.get_count_all_shop(message)
        else:
            count = user.get_count_one_shop(message)
    except e.CountNotExists:
        if all_shop:
            count = cfg.COUNT_SEARCH_ALL_SHOP
        else:
            count = cfg.COUNT_SEARCH_ONE_SHOP
    
    return count

if __name__ == "__main__":
    bot.infinity_polling()