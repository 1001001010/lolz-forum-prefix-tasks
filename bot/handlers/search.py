from bot.data.loader import dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from bot.states.user import Search
from bot.data.config import db
from bot.keyboards.inline import back_to_main_menu, search_by_egre, list_search_by_genre, seach_list_kb

@dp.callback_query_handler(text="search_genre", state="*")
async def func_search_by_egre(call: CallbackQuery, state: FSMContext):
    """
    Открытие списка жанров для поиска

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    await call.message.edit_text(f"<b>Выберите нужный жанр</b>", reply_markup=await search_by_egre())

@dp.callback_query_handler(text_startswith="searc_by_genre", state="*")
async def func_book_list_with_egre(call: CallbackQuery, state: FSMContext):
    """
    Список книг с определённым жанром

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    genre_name = call.data.split(":")[1]
    await call.message.edit_text(f"Список книг с жанром: <b>{genre_name}</b>", reply_markup=await list_search_by_genre(name = genre_name))

@dp.callback_query_handler(text="search", state="*")
async def func_books_search(call: CallbackQuery, state: FSMContext):
    """
    Поиск книг по ключевому слову или фразе

    Args:
        call (CallbackQuery)
        state (FSMContext)
    """
    await state.finish()
    await call.message.edit_text(f"Введите ключевое слово или фразу для поиска\n<b>Обратите внимание, что на поиск влияет регистр!</b>")
    await Search.word.set()

@dp.message_handler(state=Search.word)
async def func_zapros_poiska(message: Message, state: FSMContext):
    """
    Результы поиска по ключевому слову или фразе

    Args:
        message (Message)
        state (FSMContext)
    """
    await state.update_data(word=message.text)
    data = await state.get_data()
    result = await db.search_by_word(data['word'])
    if len(result) == 0:
        await message.answer('По вашему запросу ничего не найдено', reply_markup=back_to_main_menu())
    else:
        await message.answer(f"Список книг по запросу - {data['word']}", reply_markup=await seach_list_kb(data['word']))
    await state.finish()
