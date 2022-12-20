from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from Service import Texts, ReplyKeyboard, InlineKeyboard
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def main() -> None:
    executor.start_polling(dp)


@dp.message_handler(commands=['start'])
async def process_welcome(message: types.Message):
    await message.reply(Texts.WELCOME,
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


# Handlers for maker
@dp.message_handler(text=ReplyKeyboard.Text.be_maker)
async def process_maker(message: types.Message):
    # TODO Write user to database as maker
    await message.reply(Texts.WELCOME_MAKER,
                        reply_markup=ReplyKeyboard.MAKER
                        )


@dp.message_handler(text=ReplyKeyboard.Text.make_offer)
async def process_make_offer(message: types.Message):
    await message.reply(Texts.MADE_OFFER,
                        reply_markup=ReplyKeyboard.MAKER
                        )


# Handlers for taker
@dp.message_handler(text=ReplyKeyboard.Text.be_taker)
async def process_maker(message: types.Message):
    # TODO Write user to database as taker
    await message.reply(Texts.WELCOME_TAKER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


@dp.message_handler(text=ReplyKeyboard.Text.be_taker)
async def process_take_offer(message: types.Message):
    await message.reply(Texts.TAKE_OFFER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


# Common handlers
@dp.message_handler(text=ReplyKeyboard.Text.to_menu)
async def to_choose(message: types.Message):
    await message.reply("Выберите, что вас интересует",
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


if __name__ == '__main__':
    main()
