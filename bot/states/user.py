from aiogram.dispatcher.filters.state import State, StatesGroup


class New_book(StatesGroup): #State на добавление новой книги
    name = State()
    author = State()
    description = State()
    genre = State()
