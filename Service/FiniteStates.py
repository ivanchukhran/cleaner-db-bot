from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeOffer(StatesGroup):
    STATE_NAME = State()
    STATE_WEAPON = State()
    STATE_ADDRESS = State()
    STATE_COST = State()


class TakerState(StatesGroup):
    STATE_WEAPON = State()
