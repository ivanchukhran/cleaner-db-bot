from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeOffer(StatesGroup):
    STATE_NAME = State()
    STATE_WEAPON = State()
    STATE_ADDRESS = State()
    STATE_ADDITIONAL = State()
    STATE_COST = State()
