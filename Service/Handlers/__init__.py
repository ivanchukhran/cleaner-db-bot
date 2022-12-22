from aiogram import Dispatcher

from . import taker_handler, maker_handler, commands, common_handler


def setup_handlers(dp: Dispatcher):
    commands.setup(dp)
    maker_handler.setup(dp)
    taker_handler.setup(dp)
    common_handler.setup(dp)
