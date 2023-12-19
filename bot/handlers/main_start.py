from bot.data.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

@dp.message_handler(commands=['start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Ку")