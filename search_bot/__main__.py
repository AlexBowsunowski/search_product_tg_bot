from typing import List

import telebot
from snake_case.aliexpress_parser import AliexpressParser
from snake_case.shop_parser import ShopParser
from snake_case.wildberries_parser import WildberriesParser
from telebot import types

from search_bot import config as cfg
from search_bot import database as db
from search_bot import exception as e
from search_bot.callback import *

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
    keyboard = types.ReplyKeyboardMarkup(row_width=4)
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
    bot.register_next_step_handler(
        message,
        settings_callback,
        user,
        bot,
        send_keyboard,
        settings_keyboard)


@bot.message_handler(commands=['search'])
def search_keyboard(message, text="Привет, чем я могу тебе помочь?"):
    keyboard = types.ReplyKeyboardMarkup(row_width=4)
    wildberries_button = types.KeyboardButton(cfg.WILDBERRIES_BUTTON)
    aliexpress_button = types.KeyboardButton(cfg.ALIEXPRESS_BUTTON)
    allshop_button = types.KeyboardButton(cfg.ALLSHOP_BUTTON)
    exit_button = types.KeyboardButton(cfg.SEARCH_EXIT_BUTTON)

    keyboard.add(wildberries_button)
    keyboard.add(aliexpress_button)
    keyboard.add(allshop_button)
    keyboard.add(exit_button)

    message = bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    bot.register_next_step_handler(
        message, search_callback, user, bot, send_keyboard, search_keyboard)


if __name__ == "__main__":
    bot.infinity_polling()
