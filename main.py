from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from Service import setup_handlers

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def main() -> None:
    setup_handlers(dp)
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
