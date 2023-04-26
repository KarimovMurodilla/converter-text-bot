from aiogram import types

from loader import dp, db


@dp.chat_join_request_handler()
async def accept(up: types.ChatJoinRequest):  
    user_id = up.from_user.id

    if db.get_user(user_id).status == 'payed':
        await up.bot.approve_chat_join_request(up.chat.id, user_id)
        await up.bot.send_message(user_id, "Вы вступили на наш канал!")
    
