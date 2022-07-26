# SearchProduct telegram bot

Telegram-bot, который помогает искать товар в разных магазинах

На данный момент содержатся магазины:
- [Wildberries](https://www.wildberries.ru)
- [Aliexpress](https://aliexpress.ru)
### Установка

Установка необходимых библиотек `pip install -r requirements.txt`

### Общие возможности

Содержится библиотека ShopsParser, в которой содержится класс-шаблон для создания парсеров для каждого магазина. Сам телеграм-бот для поиска товара использует эту библиотеку. Есть возможность настраивать количество товаров в поиске.


