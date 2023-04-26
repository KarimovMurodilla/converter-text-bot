from aiogram import types


def cancel():
    menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
    stop = types.KeyboardButton("Bekor qilish ❌")
    menu.add(stop)

    return menu