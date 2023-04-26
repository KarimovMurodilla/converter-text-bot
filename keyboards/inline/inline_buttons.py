from aiogram import types


def select_lang():
    menu = types.InlineKeyboardMarkup(row_width=2)
    uz = types.InlineKeyboardButton("UZ", callback_data='uz')
    ru = types.InlineKeyboardButton("RU", callback_data='ru')
    en = types.InlineKeyboardButton("EN", callback_data='eng')
    menu.add(uz, ru, en)

    return menu


def admin_panel():
    menu = types.InlineKeyboardMarkup()
    stat = types.InlineKeyboardButton("Statistika", callback_data = "stat")
    msg = types.InlineKeyboardButton("Xabarnoma", callback_data = "msg")
    menu.add(stat, msg)

    return menu

def broadcast():
    menu = types.InlineKeyboardMarkup(row_width = 1)
    again = types.InlineKeyboardButton(text = "Qayta yuborish", callback_data = "msg")
    back = types.InlineKeyboardButton(text = "Orqaga", callback_data = "back")
    menu.add(again, back)

    return menu

markup_remove = types.ReplyKeyboardRemove(selective = False)


def translate():
    menu = types.InlineKeyboardMarkup(row_width=3)
    uzb = types.InlineKeyboardButton("UZ 🇺🇿", callback_data='uzb')
    rus = types.InlineKeyboardButton("RU 🇷🇺", callback_data='rus')
    eng = types.InlineKeyboardButton("EN 🇬🇧", callback_data='en')
    menu.add(uzb, rus, eng)

    return menu