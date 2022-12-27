from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class ReplyKeyboard:
    class Text:
        be_maker: str = "Хочу стать заказчиком💰"
        be_taker: str = "Хочу стать исполнителем🗡️"

        make_offer: str = "Разместить заказ💰"
        show_offers_mk: str = "Посмотреть заказы🕮"
        show_offers_tk: str = "Посмотреть заказы📖"
        take_offer: str = "Взять заказ💰"
        change_weapon: str = "Поменять оружие⚔️"
        pass_offer: str = "Сдать заказ💰"
        work_offers: str = "Взятые заказы🧳"

        to_menu: str = "Вернуться к меню🏠"
        cancel: str = "Отмена🔙"
        skip: str = "Пропустить⏭️"

    CHOOSE_SIDE = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.be_maker), KeyboardButton(Text.be_taker))

    MAKER = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.make_offer), KeyboardButton(Text.show_offers_mk)) \
        .row(KeyboardButton(Text.to_menu))

    TAKER = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.take_offer), KeyboardButton(Text.show_offers_tk)) \
        .row(KeyboardButton(Text.change_weapon), KeyboardButton(Text.pass_offer)) \
        .row(KeyboardButton(Text.work_offers), KeyboardButton(Text.to_menu))

    CANCEL = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(Text.cancel))

    CANCEL_AND_PASS = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.cancel), KeyboardButton(Text.skip))


class InlineKeyboard:
    pass
