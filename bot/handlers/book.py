from bot.data.loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from bot.states.user import New_book
from bot.data.config import db
from bot.keyboards.inline import back_to_main_menu, books_list_kb, delete_book_kb, genre_list

@dp.callback_query_handler(text="list", state="*")
async def func_books_list(call: CallbackQuery, state: FSMContext):
    """
    Вывод списка всех книг

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    await call.message.edit_text(f"Весь список книг нашей библиотеки:\n\nМожете вопспользоваться поиском по ключевым словам", reply_markup=await books_list_kb())

@dp.callback_query_handler(text_startswith="one_book", state="*")
async def func_one_book_info(call: CallbackQuery, state: FSMContext):
    """
    Открытие информации о одной книге

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    book_id = call.data.split(":")[1]
    await call.message.delete()
    book_info = await db.get_one_book(id = book_id)
    await call.message.answer(f"Название: {book_info['name']}\nАвтор: {book_info['author']}\nЖанр: {book_info['genre']}\n\nОписание: {book_info['description']}", reply_markup=await delete_book_kb(id = book_id))

@dp.callback_query_handler(text_startswith="delete", state="*")
async def func_delete_book(call: CallbackQuery, state: FSMContext):
    """
    Удаление книги

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    book_id = call.data.split(":")[1]
    await call.message.delete()
    await db.delete_book(id=book_id)
    await call.message.answer("Книга успешно удалена", reply_markup=back_to_main_menu())

@dp.callback_query_handler(text="new_book", state="*")
async def func_new_book(call: CallbackQuery, state: FSMContext):
    """
    Добавление новой книги

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    await call.message.edit_text(f"<b>Давайте добавим новую книгу!\nВведите название книги:</b>")
    await New_book.name.set()

@dp.callback_query_handler(text="new_genre", state="*")
async def func_new_genre(call: CallbackQuery):
    """
    Добавление нового жанра

    Args:
        call (CallbackQuery)
    """
    await call.message.answer("Введите новый жанр:")
    await call.message.delete()
    await New_book.genre.set()

@dp.message_handler(state=New_book.genre)
async def func_new_book_new_genre(message: Message, state: FSMContext):
    """
    Добавление новой книги с новым жанром

    Args:
        message (Message)
        state (FSMContext)
    """
    await state.update_data(genre=message.text)
    data = await state.get_data()
    await db.new_genre(name = data['genre'])
    await db.new_books(name = data['name'], author = data['author'], description = data['description'], genre = data['genre'])
    await message.answer("Книга успешно добавлена!", reply_markup=back_to_main_menu())
    await state.finish()

@dp.message_handler(state=New_book.name)
async def func_state_name(message: Message, state: FSMContext):
    """
    Ввод названия книги

    Args:
        message (Message): Название книги
        state (FSMContext)
    """
    await state.update_data(name=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь укажите автора книги:")
    await New_book.next()

@dp.message_handler(state=New_book.author)
async def func_state_author(message: Message, state: FSMContext):
    """
    Ввод автора книги

    Args:
        message (Message): Автор книги
        state (FSMContext)
    """
    await state.update_data(author=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь укажите описание книги:")
    await New_book.next()

@dp.message_handler(state=New_book.description)
async def func_state_description(message: Message, state: FSMContext):
    """
    Ввод описания книги

    Args:
        message (Message): Описание книги
        state (FSMContext)
    """
    await state.update_data(description=message.text)
    await bot.send_message(message.from_user.id, "Отлично, теперь выберите жанр или укажите свой книги:", reply_markup=await genre_list())
    await New_book.next()

@dp.callback_query_handler(text_startswith="genre:", state=New_book.genre)
async def func_new_book_to_db(call: CallbackQuery, state: FSMContext):
    """
    Информация о книге вносится в бд

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    genre_id = call.data.split(":")[1]
    await state.update_data(genre=genre_id)
    await call.message.delete()
    data = await state.get_data()
    await db.new_books(name = data['name'], author = data['author'], description = data['description'], genre = data['genre'])
    await call.message.answer("Книга успешно добавлена!", reply_markup=back_to_main_menu())
    await state.finish()
    