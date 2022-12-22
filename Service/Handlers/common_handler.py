from aiogram import Dispatcher, types

from Service import ReplyKeyboard


async def to_choose(message: types.Message):
    await message.reply("Выберите, что вас интересует",
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


async def show_offers(message: types.Message):
    # TODO Show offers for different sides
    await message.reply("Ваши заказы:",
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


def setup(dp: Dispatcher):
    dp.register_message_handler(to_choose,
                                text=ReplyKeyboard.Text.to_menu,
                                content_types=['text'],
                                state='*')
    dp.register_message_handler(show_offers,
                                text=ReplyKeyboard.Text.show_offers,
                                content_types=['text'],
                                state='*')
