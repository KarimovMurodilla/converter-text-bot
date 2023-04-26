from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, translator
from keyboards.inline import inline_buttons


@dp.callback_query_handler(state ='*')
async def queryFunc(c: types.CallbackQuery, state: FSMContext):
    user_id = c.from_user.id

    if c.data == "uz":
        db.update_lang(user_id, 'uz')
        await c.message.edit_text(
                f"Assalomu Aleykum {c.from_user.first_name}!\n"
                "Bu bot bilan siz ovozli habarlarni tekstga aylantirishingiz,\n"
                "yoki rasmdan tekstlarni olishingiz mumkin!\n\n"

                "Foydalanish uchun shunchaki ovozli habar yoki rasm jo'nating!"
            )

    elif c.data == 'ru':
        db.update_lang(user_id, 'ru')
        await c.message.edit_text(
            f'Добро пожаловать, {c.message.from_user.first_name}!\n'
            'С помощью этого бота вы можете преобразовывать\n'
            'голосовые сообщения в текст,\n'
            'или вы можете получить тексты с картинки!\n\n'

            'Отправьте голосовое сообщение или изображение, чтобы использовать бота!'
        )


    elif c.data == 'eng':
        db.update_lang(user_id, 'eng')
        await c.message.edit_text(
            f'Welcome {c.message.from_user.first_name}!'
            'With this bot you can convert voice messages into text,'
            'or you can get texts from a picture!'

            'Send a voice message or picture to use!'
        )


    # elif c.data == "stat":
    #     await message.answer(, f'Botda <b>{users[0]}</b>-ta foydalanuvchi mavjud', parse_mode = 'html' )
    
    # elif c.data == "msg":
    #     await message.answer(, "Foydalanuvchilarga yubormoqchi bo'lgan habaringizni jo'nating...", reply_markup = dont_send)
    #     bot.register_next_step_handler(c.message, MsgFunc)            
    # elif c.data == "back":
    #     bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.id, text = "Admin paneliga hush kelibsiz!", reply_markup = admin_panel)
   


    elif c.data == "uzb":
        translation = translator.translate(c.message.text, dest='uz').text
        await c.message.edit_text(text = translation, reply_markup = inline_buttons.translate())

    elif c.data == "rus":
        translation = translator.translate(c.message.text, dest='ru').text
        await c.message.edit_text(text = translation, reply_markup = inline_buttons.translate())

    elif c.data == "en":
        translation = translator.translate(c.message.text, dest='en').text
        await c.message.edit_text(text = translation, reply_markup = inline_buttons.translate())