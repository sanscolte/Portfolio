from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_phone_number() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton(text='Оправить номер телефона?', request_contact=True))
    return keyboard
