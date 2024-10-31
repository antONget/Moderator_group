from aiogram import Router, F
from aiogram.types import Message

from database import requests as rq

router = Router()
router.message.filter(F.chat.type != "private")


@router.message(F.text == '/info')
async def info(message: Message) -> None:
    your_id = message.from_user.id
    your_name = message.from_user.username
    try:
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        user = rq.get_user(tg_id=friend_id)
        if user:
            await message.answer(text=f'Ник: {user[1]}\n'
                                      f'ID: <code>{user[0]}</code>\n'
                                      f'Имя: <a href="tg://user?id={user[0]}">{user[2]}</a>\n'
                                      f'Возраст: {user[3]}\n'
                                      f'Честь: {user[4]}\n'
                                      f'В клане с {user[5]}')
        else:
            await message.answer(text='Информации о пользователе в БД нет')
    except:
        pass


