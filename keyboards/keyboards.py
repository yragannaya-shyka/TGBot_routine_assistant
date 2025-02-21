from telebot import types

def create_keyboard(buttons: list, row_width=2, resize_keyboard=True):
    keyboard = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
    keyboard.add(*buttons)
    return keyboard


def get_cancel_keyboard():
    return create_keyboard([types.KeyboardButton("Отмена")], row_width=1)
