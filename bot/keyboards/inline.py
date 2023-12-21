from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data.config import db

#Основное
def main_menu():
   """
   Создание инлайн клавиатуры | Главное меню
   """
   keyboard = InlineKeyboardMarkup()
   kb = []
   kb.append(InlineKeyboardButton("📚 Список книг", callback_data="list"))
   kb.append(InlineKeyboardButton("➕ Добавить книгу", callback_data="new_book"))
   keyboard.add(kb[0], kb[1])

   return keyboard

def back_to_main_menu():
   """
   Создание инлайн клавиатуры | Кнопка возврата в главное меню
   """
   keyboard = InlineKeyboardMarkup()
   kb = []
   kb.append(InlineKeyboardButton("В главное меню", callback_data="back_to_main_menu"))
   keyboard.add(kb[0])

   return keyboard

#Жанры
async def genre_list():
   """
   Создание инлайн клавиатуры | Список жанров и кнопка добавления нового жанра
   """
   kb = InlineKeyboardMarkup()
   list = await db.get_all_genre()
   for btn in list:
      kb.add(InlineKeyboardButton(btn['name'], callback_data=f"genre:{btn['name']}"))
   kb.add(InlineKeyboardButton("➕ Новый жанр", callback_data=f"new_genre"))

   return kb

async def search_by_egre():
   """
   Создание инлайн клавиатуры | Список жанров для поиска
   """
   kb = InlineKeyboardMarkup()
   list = await db.get_all_genre()
   for btn in list:
      kb.add(InlineKeyboardButton(btn['name'], callback_data=f"searc_by_genre:{btn['name']}"))

   return kb
#Книги
async def books_list_kb():
   """
   Создание инлайн клавиатуры | Список книг, кнопка поиска, Кнопка вывода списка с определынным жанром и кнопка возврата в главное меню
   """
   keyboard = InlineKeyboardMarkup()
   kb = []
   list = await db.get_all_books()
   kb.append(InlineKeyboardButton("🔍 Поиск", callback_data=f"search"))
   kb.append(InlineKeyboardButton("✒️ Поиск по жанру", callback_data=f"search_genre"))
   kb.append(InlineKeyboardButton("В главное меню", callback_data="back_to_main_menu"))
   keyboard.add(kb[0], kb[1])
   for btn in list:
      keyboard.add(InlineKeyboardButton(f"{btn['name']} | {btn['author']}", callback_data=f"one_book:{btn['id']}"))
   keyboard.add(kb[2])
   return keyboard

async def delete_book_kb(id):
   """
   Создание инлайн клавиатуры | Кнопка удаления книги и возврата в главное меню
   """
   kb = InlineKeyboardMarkup()
   kb.add(InlineKeyboardButton("🗑️ Удалить книгу", callback_data=f"delete:{id}"))
   kb.add(InlineKeyboardButton("В главное меню", callback_data="back_to_main_menu"))

   return kb

#Поиск
async def seach_list_kb(word):
   """
   Создание инлайн клавиатуры | Список найденных книг и кнопка возврата назад
   """
   kb = InlineKeyboardMarkup()
   list = await db.search_by_word(word)
   for btn in list:
      kb.add(InlineKeyboardButton(f"{btn['name']} | {btn['author']}", callback_data=f"one_book:{btn['id']}"))
   kb.add(InlineKeyboardButton("Назад", callback_data=f"back_to_main_menu"))

   return kb

async def list_search_by_genre(name):
   """
   Создание инлайн клавиатуры | Список книг с определыннм жанром и кнопка возврата в главное меню
   """
   kb = InlineKeyboardMarkup()
   list = await db.get_books_by_genre(name)
   if len(list) == 0:
      kb.add(InlineKeyboardButton('Ничего не найдено', callback_data="none"))
   else:
      for btn in list:
         kb.add(InlineKeyboardButton(btn['name'], callback_data=f"one_book:{btn['id']}"))
   kb.add(InlineKeyboardButton("В главное меню", callback_data="back_to_main_menu"))

   return kb