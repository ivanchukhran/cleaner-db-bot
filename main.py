from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def main() -> None:
    executor.start_polling(dp)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!")


if __name__ == '__main__':
    main()
