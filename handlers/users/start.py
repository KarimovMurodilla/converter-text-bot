from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from states.reg import Reg
from keyboards.inline import inline_buttons
from keyboards.default import keyboard_buttons

from loader import dp, db, v2t, file2text


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    from_user = message.from_user
    user = db.get_user(from_user.id)

    if not user:
        db.reg_user(from_user.id, from_user.username, None)
        await message.answer("Kerakli tilni tanlang!", reply_markup=inline_buttons.select_lang())

    else:
        if user.lang == 'uz':
            await message.answer(f"""
Assalomu Aleykum {message.from_user.first_name}!
Bu bot bilan siz ovozli habarlarni tekstga aylantirishingiz,
yoki rasmdan tekstlarni olishingiz mumkin! 

Foydalanish uchun shunchaki ovozli habar yoki rasm jo'nating""")

        elif user.lang == 'ru':
            await message.answer(f"""
Добро пожаловать, {message.from_user.first_name}!
С помощью этого бота вы можете преобразовывать 
голосовые сообщения в текст,
или вы можете получить тексты с картинки!

Отправьте голосовое сообщение или изображение, чтобы использовать бота!""")

        elif user.lang == 'en':
            await message.answer(f"""
Welcome {message.from_user.first_name}!
With this bot you can convert voice messages into text,
or you can get texts from a picture!

Send a voice message or picture to use""")


@dp.message_handler(commands = ['language'])
async def language_selection(message: types.Message):
    await message.answer(f"Kerakli tilni tanlang!\nВыберите язык!\nChoose a language!", reply_markup=inline_buttons.select_lang())


@dp.message_handler(content_types = ['voice'])
async def voice(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if not user:
        db.reg_user(user_id)
        await message.answer(f"Kerakli tilni tanlang!", reply_markup=inline_buttons.select_lang())

    else:
        try:
            down_dir = v2t.get_dir()
            await message.voice.download(f'{down_dir}/{user_id}.ogg')
            text = v2t.convert(user_id, user.lang)
            await message.reply(text, reply_markup=inline_buttons.translate())

        except Exception as e:
            print(e)
            await message.reply("Uzur... men sizni tushuna olmadim...")



@dp.message_handler(content_types = ['document'])
async def send_text_from_pdf(message: types.Message):
    user_id = message.from_user.id
    file_type = message.document.file_name.split('.')
    down_dir = file2text.get_dir()

    if file_type[1] == 'pdf':
        await message.document.download(down_dir / f'{user_id}.pdf')
        text = file2text.pdfToText(down_dir / f'{user_id}.pdf')

    elif file_type[1] == 'docx':
        await message.document.download(down_dir / f'{user_id}.docx')
        text = file2text.docxToText(down_dir / f'{user_id}.docx')
    
    await message.answer(text[0:4000], reply_markup = inline_buttons.translate())