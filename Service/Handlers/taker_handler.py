from aiogram import types, Dispatcher
from Service import ReplyKeyboard, Texts


async def process_taker(message: types.Message):
    # TODO Write user to database as taker
    await message.reply(Texts.WELCOME_TAKER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


async def process_take_offer(message: types.Message):
    # TODO write processor for listing and taking an offer
    await message.reply(Texts.TAKE_OFFER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


def setup(dp: Dispatcher):
    dp.register_message_handler(process_taker,
                                text=ReplyKeyboard.Text.be_taker,
                                content_types=['text'],
                                state='*')
    dp.register_message_handler(process_take_offer,
                                text=ReplyKeyboard.Text.take_offer,
                                content_types=['text'],
                                state='*')
