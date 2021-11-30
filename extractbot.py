import os
import time
import config
import telebot
import requests
import pytesseract
import fitz, docx
import speech_recognition as sr
from telebot import types
from connection import *
from collections import defaultdict
from googletrans import Translator

translator = Translator()


bot = telebot.TeleBot('1541736196:AAHcRjzdUnspnaD5_0hiwBsZpPlxaki-vNw')

createTable()


lang = types.InlineKeyboardMarkup(row_width=2)
uz = types.InlineKeyboardButton("UZ", callback_data='uz')
ru = types.InlineKeyboardButton("RU", callback_data='ru')
en = types.InlineKeyboardButton("EN", callback_data='en')
lang.add(uz, ru, en)


dont_send = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
stop = types.KeyboardButton("Bekor qilish ❌")
dont_send.add(stop)

admin_panel = types.InlineKeyboardMarkup()
stat = types.InlineKeyboardButton("Statistika", callback_data = "stat")
msg = types.InlineKeyboardButton("Xabarnoma", callback_data = "msg")
admin_panel.add(stat, msg)

btns = types.InlineKeyboardMarkup(row_width = 1)
again = types.InlineKeyboardButton(text = "Qayta yuborish", callback_data = "msg")
back = types.InlineKeyboardButton(text = "Orqaga", callback_data = "back")
btns.add(again, back)

markup_remove = types.ReplyKeyboardRemove(selective = False)


translate = types.InlineKeyboardMarkup(row_width=3)
uzb = types.InlineKeyboardButton("UZ 🇺🇿", callback_data='uzb')
rus = types.InlineKeyboardButton("RU 🇷🇺", callback_data='rus')
eng = types.InlineKeyboardButton("EN 🇬🇧", callback_data='eng')
translate.add(uzb, rus, eng)


def pdfToText(filename):
    with fitz.open(filename) as doc:
        text = ''
        for page in doc:
            text += page.getText()
    return text


def docxToText(docfile):
    doc = docx.Document(docfile)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


@bot.callback_query_handler(func=lambda c: True)
def queryFunc(c):
    user_id = c.from_user.id

    if c.data == "uz":
        setLang(user_id, 'uz')
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.id, text = f"""
Assalomu Aleykum {c.from_user.first_name}!
Bu bot bilan siz ovozli habarlarni tekstga aylantirishingiz,
yoki rasmdan tekstlarni olishingiz mumkin! 

Foydalanish uchun shunchaki ovozli habar yoki rasm jo'nating!""")
    elif c.data == 'ru':
        setLang(user_id, 'ru')
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.id, text = f"""
Добро пожаловать, {c.message.from_user.first_name}!
С помощью этого бота вы можете преобразовывать 
голосовые сообщения в текст,
или вы можете получить тексты с картинки!

Отправьте голосовое сообщение или изображение, чтобы использовать бота!""")
    elif c.data == 'en':
        setLang(user_id, 'en')
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.id, text = f"""
Welcome {c.message.from_user.first_name}!
With this bot you can convert voice messages into text,
or you can get texts from a picture!

Send a voice message or picture to use!""")


    elif c.data == "stat":
        con = sql.connect('users.db')
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM users")
        users = cur.fetchone()
        con.close()
        bot.send_message(c.message.chat.id, f'Botda <b>{users[0]}</b>-ta foydalanuvchi mavjud', parse_mode = 'html' )
    
    elif c.data == "msg":
        bot.send_message(c.message.chat.id, "Foydalanuvchilarga yubormoqchi bo'lgan habaringizni jo'nating...", reply_markup = dont_send)
        bot.register_next_step_handler(c.message, MsgFunc)            
    elif c.data == "back":
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.id, text = "Admin paneliga hush kelibsiz!", reply_markup = admin_panel)
   


    elif c.data == "uzb":
        translation = translator.translate(c.message.text, dest='uz').text
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text = translation, reply_markup = translate)

    elif c.data == "rus":
        translation = translator.translate(c.message.text, dest='ru').text
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text = translation, reply_markup = translate)

    elif c.data == "eng":
        translation = translator.translate(c.message.text, dest='en').text
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text = translation, reply_markup = translate)




@bot.message_handler(commands = ['help'])
def send_welcome(message):
    user_id = message.from_user.id
    if not checkUser(user_id):
        reg_user(user_id)
        bot.send_message(message.chat.id, f"Kerakli tilni tanlang!", reply_markup=lang)
    else:
        userLang = checkLang(user_id)[0]
        if userLang == 'uz':
            bot.send_message(message.chat.id, "https://telegra.ph/Botdan-foydalanish-boyicha-qollanma-06-28-2")

        elif userLang == 'ru':
            bot.send_message(message.chat.id, "https://telegra.ph/Upravlenie-botom-06-29")

        elif userLang == 'en':
            bot.send_message(message.chat.id, "https://telegra.ph/Bot-management-06-29")


@bot.message_handler(commands = ['admin'])
def send_welcome(message):
    # print(message.chat.id)
    admins = [875587704, 785550601, 1101419801]
    if message.chat.id in admins:
        bot.send_message(message.chat.id, "Admin paneliga hush kelibsiz!", reply_markup = admin_panel)

def MsgFunc(message):
    if message.text == "Bekor qilish ❌":
        bot.send_message(message.chat.id, "Habar yuborish bekor qilindi!", reply_markup = markup_remove) 

    else:
        con = sql.connect('users.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE user_id")
        user_id = cur.fetchall()
        for i in user_id:
            try:
                bot.copy_message(chat_id = i[0], from_chat_id = message.chat.id, message_id = message.message_id, reply_markup = markup_remove)
            except:
                continue

        bot.send_message(message.chat.id, "Habar yuborildi ✅", reply_markup = btns)
        con.close()





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




# @bot.message_handler(content_types = ['photo'])
# def pic(message):
#     file_info = bot.get_file(message.photo[-1].file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     src = 'result.jpg'
#     with open(src, 'wb') as new_file:
#         new_file.write(downloaded_file)

#     config = r'--oem 3 --psm 6'
#     text = (pytesseract.image_to_string('result.jpg', config = config, lang = 'Arabic+eng+rus'))
    
#     bot.send_chat_action(message.chat.id, action = 'typing')
#     time.sleep(2)
#     bot.reply_to(message, text, reply_markup = translate)


@bot.message_handler(content_types = ['voice'])
def voice(message):
    user_id = message.from_user.id

    if not checkUser(user_id):
        reg_user(user_id)
        bot.send_message(message.chat.id, f"Kerakli tilni tanlang!", reply_markup=lang)
    else:
        userLang = checkLang(user_id)[0]

        if userLang == 'uz':
            try:   
                file_info = bot.get_file(message.voice.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'result_uz.ogg'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                os.system("ffmpeg -y -i result_uz.ogg result_uz.wav")
                r = sr.Recognizer()
                file_audio = sr.AudioFile(r"result_uz.wav")
                with file_audio as source:
                    audio_text = r.record(source)

                print(type(audio_text))
                text = (r.recognize_google(audio_text, language = 'uz'))
                bot.reply_to(message, text, reply_markup = translate)
            except:
                bot.reply_to(message, "Uzur... men sizni tushuna olmadim...")


        elif userLang == 'ru':
            try:
                file_info = bot.get_file(message.voice.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'result_ru.ogg'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                os.system("ffmpeg -y -i result_ru.ogg result_ru.wav")
                r = sr.Recognizer()
                file_audio = sr.AudioFile(r"result_ru.wav")
                with file_audio as source:
                    audio_text = r.record(source)

                print(type(audio_text))
                text = (r.recognize_google(audio_text, language = 'ru'))
                bot.reply_to(message, text, reply_markup = translate)
            except:
                bot.reply_to(message, "Извините... я не смог вас распозновать...")

        elif userLang == 'en':
            try:
                file_info = bot.get_file(message.voice.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = 'result_eng.ogg'
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                os.system("ffmpeg -y -i result_eng.ogg result_eng.wav")
                r = sr.Recognizer()
                file_audio = sr.AudioFile(r"result_eng.wav")
                with file_audio as source:
                    audio_text = r.record(source)

                print(type(audio_text))
                text = (r.recognize_google(audio_text, language = 'en-US'))
                bot.reply_to(message, text, reply_markup = translate)
            except:
                bot.reply_to(message, "Sorry... I could not recognize you...")

@bot.message_handler(content_types = ['document'])
def send_text_from_pdf(message):
    file_type = message.document.file_name.split('.')

    if file_type[1] == 'pdf':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'result.pdf'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        text = pdfToText('result.pdf')
        bot.send_message(message.chat.id, text, reply_markup = translate)

    elif file_type[1] == 'docx':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'result.docx'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        text = docxToText('result.docx')
        bot.send_message(message.chat.id, text[0:4000], reply_markup = translate)



if __name__ == '__main__':
    bot.polling(none_stop = True)