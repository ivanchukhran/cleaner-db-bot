from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from Service.FiniteStates import TakerState
from Service import ReplyKeyboard, Texts

from hashlib import sha1
from config import DB_USER, DB_PASSWORD, DB_DSN
from connections.commandprocessors.commandprocessors import TakerCommandProcessor, OrderCommandProcessor
from connections.connector import Connector
from connections.queryprocessors.queryprocessors import OrderQueryProcessor


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
    name = sha1(str(message.from_user.id).encode("UTF-8")).hexdigest()
    conn = Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    taker_cp = TakerCommandProcessor(conn)
    taker_cp.create(name=name, weapon=weapon)
    await message.reply(f"Вы выбрали оружие {weapon}, вым будут предложены заказы только с ним",
                        reply_markup=ReplyKeyboard.TAKER
                        )
    await state.finish()


async def process_take_offer(message: types.Message, state: FSMContext):
    await show_offers(message)
    await TakerState.STATE_TAKE_ID.set()
    await message.reply(Texts.TAKE_OFFER,
                        reply_markup=ReplyKeyboard.CANCEL
                        )


async def process_taked_offer(message: types.Message, state: FSMContext):
    conn = Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    order_qp = OrderQueryProcessor(conn)
    user_id = sha1(str(message.from_user.id).encode("UTF-8")).hexdigest()
    orders = order_qp.get_for_taker(user_id=user_id)
    orders_id = [str(order[0]) for order in orders]
    if message.text not in orders_id:
        await message.reply("Неверный id заказа",
                            reply_markup=ReplyKeyboard.CANCEL
                            )
        await cancel(message, state)
    else:
        order_cp = OrderCommandProcessor(conn)
        order_cp.update(id=int(message.text), **{"taker_id": user_id, "status": 4})

    await state.finish()
    await message.reply(Texts.TAKED_OFFER,
                        reply_markup=ReplyKeyboard.TAKER
                        )


async def cancel(message: types.Message, state: FSMContext):
    await message.reply("Отмена",
                        reply_markup=ReplyKeyboard.TAKER
                        )
    await state.finish()


async def show_offers(message: types.Message):
    order_qp = OrderQueryProcessor(Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN))
    user_id = sha1(str(message.from_user.id).encode("UTF-8")).hexdigest()
    orders = order_qp.get_for_taker(user_id=user_id)
    orders = [f"id: {order[0]}, "
              f"victim: {order[2]}, "
              f"cost: {order[4]}, "
              f"location: {order[5]}, "
              f"weapon: {order[6]}"
              for order in orders]
    order_string = "\n".join(orders)
    await message.reply(f"Доступные заказы:\n{order_string}",
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


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
    dp.register_message_handler(show_offers,
                                text=ReplyKeyboard.Text.show_offers_tk,
                                content_types=['text'])
    dp.register_message_handler(process_taked_offer,
                                content_types=['text'],
                                state=TakerState.STATE_TAKE_ID)
