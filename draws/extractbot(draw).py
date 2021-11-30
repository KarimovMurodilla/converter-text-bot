# import fitz, docx
# import telebot
# from telebot import types
from googletrans import Translator
  
translator = Translator()  
translation = translator.translate('Hello World.', dest='ru')
print(translation.text)



# bot = telebot.TeleBot('1541736196:AAHcRjzdUnspnaD5_0hiwBsZpPlxaki-vNw')






# if __name__ == '__main__':
#     bot.polling(none_stop = True)