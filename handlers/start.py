from aiogram import Router, Bot, F, types
from aiogram.types import Message
from filter.filter_group import is_admin
from aiogram.filters import Command, CommandObject
from datetime import timedelta
from database import requests1 as rq


router = Router()
router.message.filter(F.chat.type == "private")


async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    data = await rq.parse(user_id)
    if data is None:
        await rq.create_str(user_id)
        if username:    
            await rq.username(username, user_id)
        conn.commit()
        await message.answer("Здравствуйте. Пройдите опрос через команду /opros иначе вас кикнут.")

    else:
        await message.answer(f"Здравствуйте, {data[2]}")

        # Подключаемся к базе и получаем данные о текущем пользователе
        user_data = await rq.parse(user_id)

        # Проверка на недостающие поля
        missing_fields = []
        if not user_data[1]:
            missing_fields.append("Возраст")
        if not user_data[2]:
            missing_fields.append("Nickname")
        if not user_data[3]:
            missing_fields.append("Имя")
        if not user_data[4]:
            missing_fields.append("ID")

        # Отправка сообщения о недостающих данных
        if missing_fields:
            fields_text = ", ".join(missing_fields)
            await message.answer(f"У вас не указаны следующие данные: {fields_text}.")
        await main_menu(message=message)

async def main_menu(message: types.Message):
    user_id=message.from_user.id
    data = await rq.parse(user_id)
    if not data[8]:
        kb = [
            [types.KeyboardButton(text="О клане")],
            [types.KeyboardButton(text="Правила клана")],
            [types.KeyboardButton(text="Правила пранков")],
            [types.KeyboardButton(text="Набор в клан")]
        ]
    else :
        kb = [
            [types.KeyboardButton(text="О клане")],
            [types.KeyboardButton(text="Правила клана")],
            [types.KeyboardButton(text="Правила пранков")],
            [types.KeyboardButton(text="Перевод")],
            [types.KeyboardButton(text="Рейтинг")],
            [types.KeyboardButton(text="Активности")],
            [types.KeyboardButton(text="Жалоба")],
            [types.KeyboardButton(text="Отпуск")]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(text="Вы в главном меню", reply_markup=keyboard)
