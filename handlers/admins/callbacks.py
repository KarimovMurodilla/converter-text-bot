import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline import inline_buttons



@dp.callback_query_handler(lambda c: c.data == 'withdraw_status', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    db.update_status('Вывести')
    await c.message.edit_reply_markup(reply_markup=inline_buttons.admin())


@dp.callback_query_handler(lambda c: c.data == 'top_up_status', state="*")
async def cancel_handler(c: types.CallbackQuery, state: FSMContext):
    db.update_status('Пополнить')
    await c.message.edit_reply_markup(reply_markup=inline_buttons.admin())