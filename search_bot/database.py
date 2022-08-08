import sqlite3

from itertools import chain
from typing import List, Tuple
from search_bot import config as cfg
from search_bot import exception as e


class User:
    """ 
    Класс User для работе с базой данных, которая содержит информацию
    о userid, число продуктов, которые надо выдать пользователю при поиске в случае
    если идет поиск по одному магазину или идет поиск по всем магазинам
    """

    def __init__(self, db_name: str = cfg.DB_NAME) -> None:
        self.db_name = db_name
        self._create_table()

    def _create_table(self) -> None:
        """ 
        Создаем таблицу с названием self.db_name, если до этого не была создана
        """
        with sqlite3.connect(self.db_name) as conn:
            query = """
                CREATE TABLE IF NOT EXISTS user(
                    userid INT,
                    count_product_one_shop INT,
                    count_product_all_shop INT
                )
            """
            conn.execute(query)

    def set_count_one_shop(self, message) -> None:
        """ 
        Устанавливаем число товаров на один магазин
        """
        count = int(message.text)
        with sqlite3.connect(self.db_name) as conn:

            if self._exist_user_count(message):
                conn.execute(
                    "INSERT INTO user VALUES (?, ?, ?)",
                    (message.chat.id, count, cfg.COUNT_SEARCH_ALL_SHOP,)
                )
            else:
                query = """
                    UPDATE user 
                    SET count_product_one_shop=?
                    WHERE userid=?
                """
                conn.execute(
                    query,
                    (count, message.chat.id)
                )

    def set_count_all_shop(self, message) -> None:
        """ 
        Устанавливаем число товаров на все магазины
        """
        count = int(message.text)
        with sqlite3.connect(self.db_name) as conn:

            if self._exist_user_count(message):
                conn.execute(
                    "INSERT INTO user VALUES (?, ?, ?)",
                    (message.chat.id, cfg.COUNT_SEARCH_ONE_SHOP, count)
                )
            else:
                query = """
                    UPDATE user 
                    SET count_product_all_shop=?
                    WHERE userid=?
                """
                conn.execute(
                    query,
                    (count, message.chat.id)
                )

    def get_count_one_shop(self, message) -> int:
        """ 
        Выдаем число товаров на один магазин
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT count_product_one_shop FROM user WHERE userid=?",
                (message.chat.id,),
            )
            count: List[Tuple[int]] = cur.fetchall()
            count: List[str] = list(chain.from_iterable(count))
            if len(count) == 0:
                raise e.CountNotExists

            return count[0]

    def get_count_all_shop(self, message) -> int:
        """ 
        Устанавливаем число товаром на один магазин
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT count_product_all_shop FROM user WHERE userid=?",
                (message.chat.id,),
            )
            count: List[Tuple[int]] = cur.fetchall()
            count: int = list(chain.from_iterable(count))
            if len(count) == 0:
                raise e.CountNotExists

            return count[0]

    def _exist_user_count(self, message) -> bool:
        """ 
        Проверяем наличие пользователя в базе данных
        """
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM user WHERE userid=?",
                (message.chat.id,)
            )
            user: List[Tuple[int, int, int]] = cur.fetchall()
            return len(user) == 0
