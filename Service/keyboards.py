from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class ReplyKeyboard:
    class Text:
        be_maker: str = "Хочу стать заказчиком💰"
        be_taker: str = "Хочу стать исполнителем🗡️"

        make_offer: str = "Разместить заказ💰"
        show_offers: str = "Посмотреть заказы🕮"
        take_offer: str = "Взять заказ💰"

        to_menu: str = "Вернуться к меню🏠"
        cancel: str = "Отмена🔙"

    CHOOSE_SIDE = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.be_maker), KeyboardButton(Text.be_taker))

    MAKER = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.make_offer), KeyboardButton(Text.show_offers)) \
        .row(KeyboardButton(Text.to_menu))

    TAKER = ReplyKeyboardMarkup(resize_keyboard=True) \
        .row(KeyboardButton(Text.take_offer), KeyboardButton(Text.show_offers)) \
        .row(KeyboardButton(Text.to_menu))

    CANCEL = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(Text.cancel))


class InlineKeyboard:
    pass
