from aiogram import types, Dispatcher

from Service import ReplyKeyboard, Texts


async def process_maker(message: types.Message):
    # TODO Write user to database as maker
    await message.reply(Texts.WELCOME_MAKER,
                        reply_markup=ReplyKeyboard.MAKER
                        )


async def process_make_offer(message: types.Message):
    await message.reply(Texts.MADE_OFFER,
                        reply_markup=ReplyKeyboard.MAKER
                        )


def setup(dp: Dispatcher):
    dp.register_message_handler(process_maker,
                                text=ReplyKeyboard.Text.be_maker,
                                content_types=['text'],
                                state='*')
    dp.register_message_handler(process_make_offer,
                                text=ReplyKeyboard.Text.make_offer,
                                content_types=['text'],
                                state='*')
