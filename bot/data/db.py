import aiosqlite
from async_class import AsyncClass

path_db = 'bot/data/database.db'

def dict_factory(cursor, row):
    """Преобразование результата в словарь

    Args:
        cursor: Объект курсора
        row: Результат запроса

    Returns:
        Словарь
    """
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

class DB(AsyncClass):
    async def __ainit__(self):
        self.con = await aiosqlite.connect(path_db)
        self.con.row_factory = dict_factory
        
    async def create_db(self):
        book_info = await self.con.execute("PRAGMA table_info(book)")
        if len(await book_info.fetchall()) == 5:
            print("database was found (Book | 1/2)")
        else:
            await self.con.execute("CREATE TABLE book("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "name TEXT,"
                                   "author TEXT,"
                                   "description TEXT,"
                                   "genre TEXT)")
            print("database was not found (Book | 1/2), creating...")

        genre_info = await self.con.execute("PRAGMA table_info(genre)")
        if len(await genre_info.fetchall()) == 2:
            print("database was found (Genre | 1/2)")
        else:
            await self.con.execute("CREATE TABLE genre("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "name TEXT)")
            print("database was not found (Genre | 2/2), creating...")