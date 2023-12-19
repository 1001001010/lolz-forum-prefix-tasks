from bot.data.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import main_menu
@dp.message_handler(commands=['start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Доброо пожаловать в базу управления книгами\n\nВы можете:\nОсуществлять поиск по ключевым словам\nДобавлять свои книги\nУдалять книги", reply_markup=main_menu())