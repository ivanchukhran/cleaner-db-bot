from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from Service.FiniteStates import TakerState
from Service import ReplyKeyboard, Texts


async def process_taker(message: types.Message):
    await message.reply(Texts.WELCOME_TAKER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


async def change_weapon(message: types.Message, state: FSMContext):
    await message.reply("Введите оружие, которым вы владеете лучше всего:",
                        reply_markup=ReplyKeyboard.CANCEL
                        )
    await TakerState.STATE_WEAPON.set()


async def process_changing(message: types.Message, state: FSMContext):
    weapon = message.text.lower()
    # TODO saving weapon with person to db
    await message.reply(f"Вы выбрали оружие {weapon}, вым будут предложены заказы только с ним",
                        reply_markup=ReplyKeyboard.TAKER
                        )
    await state.finish()


async def process_take_offer(message: types.Message):
    # TODO write processor for listing and taking an offer
    await message.reply(Texts.TAKE_OFFER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


async def cancel(message: types.Message, state: FSMContext):
    await message.reply("Отмена",
                        reply_markup=ReplyKeyboard.TAKER
                        )
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(process_taker,
                                text=ReplyKeyboard.Text.be_taker,
                                content_types=['text'])
    dp.register_message_handler(process_take_offer,
                                text=ReplyKeyboard.Text.take_offer,
                                content_types=['text'])
    dp.register_message_handler(change_weapon,
                                text=ReplyKeyboard.Text.change_weapon,
                                content_types=['text'])
    dp.register_message_handler(cancel,
                                text=ReplyKeyboard.Text.cancel,
                                content_types=['text'],
                                state="*")
    dp.register_message_handler(process_changing,
                                content_types=['text'],
                                state=TakerState.STATE_WEAPON)
