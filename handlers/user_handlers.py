from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart

from database import requests as rq
from keyboards.keyboard import main_keyboard
import logging
from utils.error_handling import error_handler

router = Router()
router.message.filter(F.chat.type == "private")


# Определение состояний
class Registration(StatesGroup):
    name = State()
    age = State()


@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
@router.message(F.text == '/get_dbfile')
@error_handler
async def process_press_start(message: Message, bot: Bot) -> None:
    """
    Обработка команды /start и 'Главное меню'
    :param message:
    :param bot:
    :return:
    """
    logging.info('process_press_start ')
    if message.text == '/get_dbfile':
        file_path = "database/db.sqlite3"
        await message.answer_document(FSInputFile(file_path))
        return
    tg_id: int = message.from_user.id
    username: str = message.from_user.username
    user = await rq.get_user_tg_id(tg_id=tg_id)
    # добавление или обновление пользователя в БД
    if not user:
        if not username:
            username = 'Username'
        data = {"tg_id": message.chat.id, "username": username}
        await rq.add_new_user(data=data)
    # обновление username
    elif username != user.username:
        await rq.update_username(tg_id=message.from_user.id,
                                 username=message.from_user.username)
    # else:
    #     # Проверка на недостающие поля
    #     missing_fields = []
    #     if not user.age:
    #         missing_fields.append("Возраст")
    #     if not user.nickname:
    #         missing_fields.append("Nickname")
    #     if not user.name:
    #         missing_fields.append("Имя")
    #     if not user.id_PUBG_MOBILE:
    #         missing_fields.append("ID")
    #
    #     # Отправка сообщения о недостающих данных
    #     if missing_fields:
    #         fields_text = ", ".join(missing_fields)
    #         await message.answer(f"У вас не указаны следующие данные: {fields_text} \n"
    #                              f"Заполните их применив команду /opros")
    # получаем список групп
    groups = await rq.get_groups()
    # флаг того что пользователь состоит в группе
    auth = False
    for group in groups:
        member = await bot.get_chat_member(user_id=message.from_user.id,
                                           chat_id=group.group_id)
        if member.status != 'left':
            auth = True
    # получаем данные о пользователе
    user = await rq.get_user_tg_id(tg_id=tg_id)
    # выводим клавиатуру для авторизованных и нет пользователей
    if user.name:
        await message.answer(f"Здравствуйте, {user.name}",
                             reply_markup=main_keyboard(auth=auth))
    else:
        await message.answer(f"Здравствуйте!",
                             reply_markup=main_keyboard(auth=auth))
    # если пользователь не состоит в группе то предлагаем пройти опрос
    if auth:
        await message.answer(
            "Здравствуйте. Пройдите опрос через команду /opros, чтобы получить ссылку на основной чат.")
