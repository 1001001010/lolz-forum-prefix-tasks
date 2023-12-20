from bot.data.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import main_menu, genre_list
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
    await message.answer(f"name: {data['name']}\n"
                         f"author: {data['author']}\n"
                         f"description: {data['description']}\n"
                         f"genre: {data['genre']}")
    await state.finish()
# @dp.message_handler(state=New_book.genre)
# async def state_genre(message: types.Message, state: FSMContext):
#     await message.answer("список имеющихся жанров: ", reply_markup=genre_list())

    # await state.update_data(genre=message.text)
    # data = await state.get_data()
    # await message.answer(f"name: {data['name']}\n"
    #                      f"author: {data['author']}\n"
    #                      f"description: {data['description']}\n"
    #                      f"genre: {data['genre']}")

    # await state.finish()