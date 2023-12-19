import colorama
import asyncio
import logging

from aiogram import executor, Dispatcher
from bot.handlers import dp
from bot.data.config import db
from bot.data.loader import scheduler

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
colorama.init()


async def on_startup(dp: Dispatcher):
    """Выполнение функции после запуска бота

    Args:
        dp (Dispatcher)
    """

    print(colorama.Fore.GREEN + "=======================")
    print(colorama.Fore.RED + "Бот успешно запущен")
    print(colorama.Fore.LIGHTBLUE_EX + "Разработчик: https://t.me/lll10010010")
    print(colorama.Fore.RESET)

async def on_shutdown(dp: Dispatcher):
    """Выполнение функции после выключения бота

    Args:
        dp (Dispatcher)
    """

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()


if __name__ == "__main__":
    scheduler.start()
    loop = asyncio.get_event_loop()
    loop.create_task(db.create_db())
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)