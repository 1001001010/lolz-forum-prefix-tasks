from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    """Создание инлайн клавиатуры | main

    Returns:
       inline клавиатура | main
    """
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("📚 Список книг", callback_data="list"))
    kb.append(InlineKeyboardButton("➕ Добавить книгу", callback_data="list"))

    keyboard.add(kb[0], kb[1])

    return keyboard