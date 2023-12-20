from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data.config import db

def main_menu():
    """Создание инлайн клавиатуры | main

    Returns:
       inline клавиатура | main
    """
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("📚 Список книг", callback_data="list"))
    kb.append(InlineKeyboardButton("➕ Добавить книгу", callback_data="new_book"))

    keyboard.add(kb[0], kb[1])

    return keyboard

async def genre_list():
   kb = InlineKeyboardMarkup()
   list = await db.get_all_genre()
   for btn in list:
      kb.add(InlineKeyboardButton(btn['name'], callback_data=f"genre:{btn['name']}"))
   kb.add(InlineKeyboardButton("➕ Новый жанр", callback_data=f"new_genre"))

   return kb