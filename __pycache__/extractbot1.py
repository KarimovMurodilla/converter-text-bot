import os
import config
import telebot
import requests
import pytesseract
import speech_recognition as sr
from telebot import types
from connection import *
from collections import defaultdict


pytesseract.pytesseract.tesseract_cmd = config.path

bot = telebot.TeleBot(config.token)

createTable()



lang = types.InlineKeyboardMarkup(row_width=2)
uz = types.InlineKeyboardButton("UZ", callback_data='uz')
ru = types.InlineKeyboardButton("RU", callback_data='ru')
en = types.InlineKeyboardButton("EN", callback_data='en')
lang.add(uz, ru, en)




@bot.callback_query_handler(func=lambda c: True)
def queryFunc(c):
    user_id = c.from_user.id

    if c.data == "uz":
        setLang(user_id, 'uz')
        bot.send_message(c.message.chat.id, f"""
        Assalomu Aleykum {c.from_user.first_name}!
        Bu bot bilan siz ovozli habarlarni tekstga aylantirishingiz,
        yoki rasmdan tekstlarni olishingiz mumkin! 

        Foydalanish uchun shunchaki ovozli habar yoki rasm jo'nating""")
    elif c.data == 'ru':
        setLang(user_id, 'ru')
        bot.send_message(c.message.chat.id, f"Привет")
    elif c.data == 'en':
        setLang(user_id, 'en')
        bot.send_message(c.message.chat.id, f"Hello")


@bot.message_handler(commands = ['language'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Kerakli tilni tanlang!\nВыберите язык!\nChoose a language!", reply_markup=lang)


@bot.message_handler(commands = ['start'])
def send_welcome(message):
    user_id = message.from_user.id

    if not checkUser(user_id):
        reg_user(user_id)
        bot.send_message(message.chat.id, f"Kerakli tilni tanlang!", reply_markup=lang)
    else:
        userLang = checkLang(user_id)[0]

        if userLang == 'uz':
            bot.send_message(message.chat.id, f"""
Assalomu Aleykum {message.from_user.first_name}!
Bu bot bilan siz ovozli habarlarni tekstga aylantirishingiz,
yoki rasmdan tekstlarni olishingiz mumkin! 

Foydalanish uchun shunchaki ovozli habar yoki rasm jo'nating""")
        elif userLang == 'ru':
            bot.send_message(message.chat.id, f"""
Добро пожаловать, {message.from_user.first_name}!
С помощью этого бота вы можете преобразовывать 
голосовые сообщения в текст,
или вы можете получить тексты с картинки!

Отправьте голосовое сообщение или изображение, чтобы использовать бота!""")

        elif userLang == 'en':
            bot.send_message(message.chat.id, f"""
Welcome {message.from_user.first_name}!
With this bot you can convert voice messages into text,
or you can get texts from a picture!

Send a voice message or picture to use""")




@bot.message_handler(content_types = ['photo'])
def pic(message):
    file_info = bot.get_file(message.photo[2].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'result.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    text = (pytesseract.image_to_string(r'result.jpg'))
    bot.reply_to(message, text)


@bot.message_handler(content_types = ['voice'])
def voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'result.ogg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    os.system("ffmpeg -y -i result.ogg result.wav")
    r = sr.Recognizer()
    file_audio = sr.AudioFile(r"result.wav")
    with file_audio as source:
        audio_text = r.record(source)

    print(type(audio_text))
    text = (r.recognize_google(audio_text, language = 'uz'))
    bot.reply_to(message, text)






if __name__ == '__main__':
    bot.polling(none_stop = True)