# - *- coding: utf- 8 - *-
import configparser
from bot.data.db import DB
import asyncio

async def main_db():
    """
    Создание экземпляра бд 
    """
    db = await DB()

    return db


loop = asyncio.get_event_loop()
task = loop.create_task(main_db())
db = loop.run_until_complete(task)

read_config = configparser.ConfigParser()
read_config.read("settings.ini")

bot_token = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
path_database = "tgbot/data/database.db"  # Путь к Базе Данных
