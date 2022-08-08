from typing import List

from snake_case.aliexpress_parser import AliexpressParser
from snake_case.shop_parser import ShopParser
from snake_case.wildberries_parser import WildberriesParser
from telebot import types

from search_bot import exception as e

from search_bot import config as cfg


def settings_callback(message, user, bot, next_callback, back_callback):
    if message.text == cfg.SETTING_ONE_SHOP_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Введите число продуктов"
        )
        bot.register_next_step_handler(
            message,
            set_settings,
            type_of_set=cfg.SETTING_ONE_SHOP_BUTTON,
            user=user,
            next_callback=back_callback)
    elif message.text == cfg.SETTING_ALL_SHOP_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Введите число продуктов"
        )
        bot.register_next_step_handler(
            message,
            set_settings,
            type_of_set=cfg.SETTING_ALL_SHOP_BUTTON,
            user=user,
            next_callback=back_callback)

    elif message.text == cfg.SETTING_LOOK_BUTTON:
        settings = get_settings(message, user)
        message = bot.send_message(
            message.chat.id,
            text=f"Ваши текущие настройки:\n{settings}"
        )
        back_callback(
            message=message,
            text="Возвращаемся к настройкам:")
    elif message.text == cfg.SETTING_EXIT_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Выходим из настроек"
        )
        next_callback(
            message=message,
            text="Команды бота:")


def set_settings(message, type_of_set, user, next_callback):
    if type_of_set == cfg.SETTING_ONE_SHOP_BUTTON:
        user.set_count_one_shop(message=message)

    elif type_of_set == cfg.SETTING_ALL_SHOP_BUTTON:
        user.set_count_all_shop(message=message)
    next_callback(
        message=message,
        text="Возвращаемся к настройкам:")


def get_settings(message, user):
    result = "Количество товаров при поиске по одному магазину: {count_one}\n"\
        "Количество товаров при поиске по всем магазинам: {count_all}"
    try:
        count_one = user.get_count_one_shop(message=message)
        count_all = user.get_count_all_shop(message=message)
    except e.CountNotExists:
        count_one = cfg.COUNT_SEARCH_ONE_SHOP
        count_all = cfg.COUNT_SEARCH_ALL_SHOP

    return result.format(count_one=count_one, count_all=count_all)


def search_callback(message, user, bot, next_callback, back_callback):
    if message.text == cfg.WILDBERRIES_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.WILDBERRIES_BUTTON,
            user,
            bot,
            back_callback)
    elif message.text == cfg.ALIEXPRESS_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.ALIEXPRESS_BUTTON,
            user,
            bot,
            back_callback)
    elif message.text == cfg.ALLSHOP_BUTTON:
        message = bot.send_message(
            chat_id=message.chat.id,
            text="Введите название товара"
        )
        bot.register_next_step_handler(
            message,
            search,
            cfg.ALLSHOP_BUTTON,
            user,
            bot,
            back_callback)
    elif message.text == cfg.SEARCH_EXIT_BUTTON:
        message = bot.send_message(
            message.chat.id,
            text="Выходим из поиска"
        )
        next_callback(
            message=message,
            text="Команды бота:")


def search(message, shop, user, bot, next_callback):
    results = []
    bot.send_message(
        chat_id=message.chat.id,
        text="Ищу...",
    )
    count = count_parsing(message, user, shop == cfg.ALLSHOP_BUTTON)
    product = message.text.strip().replace(" ", "%20")
    if shop == cfg.WILDBERRIES_BUTTON or shop == cfg.ALLSHOP_BUTTON:
        parser_shop = WildberriesParser()
        result = get_products(parser_shop=parser_shop,
                              name_product=product, count_product=count)
        results.extend(result)
    if shop == cfg.ALIEXPRESS_BUTTON or shop == cfg.ALLSHOP_BUTTON:
        parser_shop = AliexpressParser()
        result = get_products(parser_shop=parser_shop,
                              name_product=product, count_product=count)
        results.extend(result)

    send_products(message=message, products=results, bot=bot)

    next_callback(
        message=message,
        text="Чем еще могу помочь?"
    )


def send_products(message, products, bot):
    for product in products:
        bot.send_message(
            chat_id=message.chat.id,
            text=product.tlg_repr()
        )
        bot.send_photo(
            message.chat.id,
            product.image,
        )


def get_products(
        parser_shop: ShopParser,
        name_product: str,
        count_product: int) -> List:
    page = 1
    total = 0
    result = []
    while count_product != total:
        products = parser_shop.run(
            name_product, page=page, count=count_product - total)
        if len(products) == 0:
            break
        total += len(products)
        result.extend(products)
        page += 1
    return result


def count_parsing(message, user, all_shop=False) -> int:
    count = 0
    try:
        count = user.get_count_all_shop(
            message) if all_shop else user.get_count_one_shop(message)
    except e.CountNotExists:
        count = cfg.COUNT_SEARCH_ALL_SHOP if all_shop else cfg.COUNT_SEARCH_ONE_SHOP
    return count
