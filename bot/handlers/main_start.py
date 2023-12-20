from bot.data.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import main_menu, genre_list, back_to_main_menu, books_list_kb
from bot.states.user import New_book
from bot.data.config import db

@dp.message_handler(commands=['start'], state="*")
async def main_start(message: Message, state: FSMContext):
    """Действие на комманду /start

    Args:
        message (Message)
        state (FSMContext)
    """
    await state.finish()
    await bot.send_message(message.from_user.id, "Доброо пожаловать в базу управления книгами\n\nВы можете:\nОсуществлять поиск по ключевым словам\nДобавлять свои книги\nУдалять книги", reply_markup=main_menu())

@dp.callback_query_handler(text="list", state="*")
async def books_list(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"Весь список книг нашей библиотеки:\n\nМожете вопспользоваться поиском по ключевым словам", reply_markup=await books_list_kb())

@dp.callback_query_handler(text_startswith="one_book", state="*")
async def one_book_info(call: CallbackQuery, state: FSMContext):
    await state.finish()
    book_id = call.data.split(":")[1]
    book_info = await db.get_one_book(id = book_id)
    await call.message.answer(f"Название: {book_info['name']}\nАвтор: {book_info['author']}\nЖанр: {book_info['genre']}\n\nОписание: {book_info['description']}")

@dp.callback_query_handler(text="new_book", state="*")
async def new_book(call: CallbackQuery, state: FSMContext):
    """Добавление новой книги

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    await call.message.edit_text(f"<b>Давайте добавим новую книгу!\nВведите название книги:</b>")
    await New_book.name.set()

@dp.message_handler(state=New_book.name)
async def state_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь укажите автора книги:")
    await New_book.next()

@dp.message_handler(state=New_book.author)
async def state_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь укажите описание книги:")
    await New_book.next()

@dp.message_handler(state=New_book.description)
async def state_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь выберите жанр или укажите свой книги:", reply_markup=await genre_list())
    await New_book.next()

@dp.callback_query_handler(text_startswith="genre:", state=New_book.genre)
async def new_book(call: CallbackQuery, state: FSMContext):
    genre_id = call.data.split(":")[1]
    await state.update_data(genre=genre_id)
    await call.message.delete()
    data = await state.get_data()
    await db.new_books(name = data['name'], author = data['author'], description = data['description'], genre = data['genre'])
    await call.message.answer("Книга успешно добавлена!", reply_markup=back_to_main_menu())
    await state.finish()
    
@dp.callback_query_handler(text="new_genre", state="*")
async def new_book(call: CallbackQuery):
    await call.message.answer("Введите новый жанр:")
    await call.message.delete()
    await New_book.genre.set()

@dp.message_handler(state=New_book.genre)
async def state_description(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    await db.new_genre(name = data['genre'])
    await db.new_books(name = data['name'], author = data['author'], description = data['description'], genre = data['genre'])
    await message.answer("Книга успешно добавлена!", reply_markup=back_to_main_menu())
    await state.finish()

@dp.callback_query_handler(text="back_to_main_menu", state="*")
async def back_to_menu(call: CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "Доброо пожаловать в базу управления книгами\n\nВы можете:\nОсуществлять поиск по ключевым словам\nДобавлять свои книги\nУдалять книги", reply_markup=main_menu())
