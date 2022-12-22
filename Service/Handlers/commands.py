import aiogram
from aiogram import Dispatcher

from Service import Texts, ReplyKeyboard


async def start(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await message.reply(Texts.WELCOME,
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


def setup(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
