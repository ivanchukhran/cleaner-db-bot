from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from Service.FiniteStates import MakeOffer
from Service import ReplyKeyboard, Texts

from hashlib import sha1

from config import DB_DSN, DB_USER, DB_PASSWORD
from connections.connector import Connector
from connections.commandprocessors.commandprocessors import MakerCommandProcessor, OrderCommandProcessor
from connections.queryprocessors.queryprocessors import OrderQueryProcessor


async def process_maker(message: types.Message):
    conn = Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    maker_cp = MakerCommandProcessor(conn)
    name: str = sha1(str(message.from_user.id).encode("UTF-8")).hexdigest()
    maker_cp.create(name)
    await message.reply(Texts.WELCOME_MAKER,
                        reply_markup=ReplyKeyboard.MAKER
                        )


async def process_make_offer(message: types.Message, state: FSMContext):
    await message.reply("Вы решили сделать заказ, укажите имя жертвы:",
                        reply_markup=ReplyKeyboard.CANCEL
                        )
    await MakeOffer.STATE_NAME.set()


async def process_write_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Выберите оружие, которым должен быть выполнен заказ:",
                         reply_markup=ReplyKeyboard.CANCEL)
    await MakeOffer.STATE_WEAPON.set()


async def process_write_weapon(message: types.Message, state: FSMContext):
    await state.update_data(weapon=message.text)
    await message.answer("Введите локацию, где это должно произойти:",
                         reply_markup=ReplyKeyboard.CANCEL)
    await MakeOffer.STATE_ADDRESS.set()


async def process_write_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Напишите цену, которую готовы заплатить:",
                         reply_markup=ReplyKeyboard.CANCEL)
    await MakeOffer.STATE_COST.set()


async def process_write_offer(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        cost = int(message.text)
        offer_data = await state.get_data()
        conn = Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        order_cp = OrderCommandProcessor(conn)
        order_cp.create(maker=sha1(str(message.from_user.id).encode("UTF-8")).hexdigest(),
                        victim=offer_data['name'],
                        weapon=offer_data['weapon'],
                        cost=cost,
                        location=offer_data['location'])
        await message.answer(
            f"Ваш заказ на {offer_data['name']} с использованием {offer_data['weapon']} за {cost} выставлен на рынок",
            reply_markup=ReplyKeyboard.MAKER)
        await state.finish()
    else:
        await message.answer("Введенное значение не является числом, повторите еще раз",
                             reply_markup=ReplyKeyboard.CANCEL)


async def cancel(message: types.Message, state: FSMContext):
    await message.reply("Отмена",
                        reply_markup=ReplyKeyboard.MAKER
                        )
    await state.finish()


async def show_offers(message: types.Message):
    conn = Connector(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    order_qp = OrderQueryProcessor(conn)
    orders = order_qp.get_by_maker(sha1(str(message.from_user.id).encode("UTF-8")).hexdigest())
    if orders:
        print(orders[0][0])
    orders = [f"Заказ на {order[0]} за {order[3]}" for order in orders]
    orders_string = "\n".join(orders)
    await message.reply(f"Ваши заказы:\n{orders_string}",
                        reply_markup=ReplyKeyboard.CHOOSE_SIDE
                        )


def setup(dp: Dispatcher):
    dp.register_message_handler(process_maker,
                                text=ReplyKeyboard.Text.be_maker,
                                content_types=['text'])
    dp.register_message_handler(process_make_offer,
                                text=ReplyKeyboard.Text.make_offer,
                                content_types=['text'])
    dp.register_message_handler(cancel,
                                text=ReplyKeyboard.Text.cancel,
                                content_types=['text'],
                                state="*")
    dp.register_message_handler(process_write_name,
                                content_types=['text'],
                                state=MakeOffer.STATE_NAME)
    dp.register_message_handler(process_write_weapon,
                                content_types=['text'],
                                state=MakeOffer.STATE_WEAPON)
    dp.register_message_handler(process_write_location,
                                content_types=['text'],
                                state=MakeOffer.STATE_ADDRESS)
    dp.register_message_handler(process_write_offer,
                                content_types=['text'],
                                state=MakeOffer.STATE_COST)
    dp.register_message_handler(show_offers,
                                text=ReplyKeyboard.Text.show_offers_mk,
                                content_types=['text'],)
