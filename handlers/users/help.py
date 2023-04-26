from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, db
from keyboards.inline import inline_buttons


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        db.reg_user(user_id, None)
        await message.answer(f"Kerakli tilni tanlang!", reply_markup=inline_buttons.select_lang())

    else:
        if user.lang == 'uz':
            await message.answer("https://telegra.ph/Botdan-foydalanish-boyicha-qollanma-06-28-2")

        elif user.lang == 'ru':
            await message.answer("https://telegra.ph/Upravlenie-botom-06-29")

        elif user.lang == 'en':
            await message.answer("https://telegra.ph/Bot-management-06-29")
