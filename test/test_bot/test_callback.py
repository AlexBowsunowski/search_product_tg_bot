import sqlite3
from unittest import mock
import unittest
import pytest
import time
import telebot
from search_bot import config as cfg
from search_bot import database as db
from search_bot.callback import *
from snake_case import wildberries_parser
from snake_case.aliexpress_parser import AliexpressParser
from snake_case.item import Item
from snake_case.wildberries_parser import WildberriesParser
from telebot import types


def next_callback(message, text):
    pass


class TestCallback(unittest.TestCase):
    def setUp(self):
        self.user = db.User('test_user.db')
        self.bot = telebot.TeleBot(cfg.TOKEN)
        self.msg = self.create_text_message('')
        self.item1_ali = Item(shop_name="www.aliexpress.ru",
                              brand_name="realus Store",
                              goods_name="Смарт-часы Honor Watch GS Pro, SpO2, пульсометр, Bluetooth, 1,39 дюйма, AMOLED, 5 атм",
                              price=9566.20,
                              url="https://aliexpress.ru/item/1005003933434816.html?sku_id=12000028898990402",
                              image="https://ae04.alicdn.com/kf/S3522ccf1ab3a4a04a68622ddfa23d7f7p/Honor-Watch-GS-Pro-Smart-Watch-SpO2-Smartwatch-Heart-Rate-Monitoring-Bluetooth-Call-1-39-AMOLED.jpg_480x480q55.jpg")
        self.item1_wild = Item(shop_name="www.wildberries.ru",
                               brand_name="Honor",
                               goods_name="Ноутбук",
                               price=45553.0,
                               url="https://www.wildberries.ru/catalog/54392459/detail.aspx?targetUrl=BP",
                               image="https://images.wbstatic.net/c516x688/new/54390000/54392459-1.jpg")

    def tearDown(self):
        pass

    def test_message_settings_handler(self):
        """ 
        Тестируем set_settings, get_settings, count_parsings
        """
        self.msg.text = "10"
        check = 'Количество товаров при поиске по одному магазину: {count_one}\nКоличество товаров при поиске по всем магазинам: {count_all}'
        count_one = 5
        count_all = 2

        results = get_settings(self.msg, self.user)
        assert results == check.format(
            count_one=count_one, count_all=count_all)
        count_one_parsing = count_parsing(self.msg, self.user)
        assert count_one_parsing == count_one
        count_all_parsing = count_parsing(self.msg, self.user, True)
        assert count_all_parsing == count_all

        set_settings(self.msg, cfg.SETTING_ONE_SHOP_BUTTON,
                     self.user, next_callback)
        count_one = 10
        results = get_settings(self.msg, self.user)
        assert results == check.format(
            count_one=count_one, count_all=count_all)
        count_one_parsing = count_parsing(self.msg, self.user)
        assert count_one_parsing == count_one
        count_all_parsing = count_parsing(self.msg, self.user, True)
        assert count_all_parsing == count_all

        self.msg.text = "5"
        set_settings(self.msg, cfg.SETTING_ALL_SHOP_BUTTON,
                     self.user, next_callback)
        count_all = 5
        results = get_settings(self.msg, self.user)
        assert results == check.format(
            count_one=count_one, count_all=count_all)
        count_one_parsing = count_parsing(self.msg, self.user)
        assert count_one_parsing == count_one
        count_all_parsing = count_parsing(self.msg, self.user, True)
        assert count_all_parsing == count_all

    def test_wild_get_products_handler(self):
        products = get_products(WildberriesParser(), 'honor', 1)
        assert products[0] == self.item1_wild

    def test_ali_get_products_handler(self):

        products = get_products(AliexpressParser(), 'honor', 1)

        assert products[0] == self.item1_ali

    @staticmethod
    def create_text_message(text):
        params = {'text': text}
        chat = types.User(11, False, 'test')
        return types.Message(1, None, None, chat, 'text', params, '')
