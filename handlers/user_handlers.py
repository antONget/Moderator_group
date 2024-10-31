import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter, CommandStart
from database import requests as rq

router = Router()
# Текст приветствия
start_text = """
Добро пожаловать! Вас приветствует БОТ! Пройдите регистрацию по ссылке {ссылка}.
"""


# Определение состояний
class Registration(StatesGroup):
    name = State()
    age = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    """
    Запуск бота
    :param message:
    :param state:
    :return:
    """
    tg_id = message.chat.id
    await state.set_state(state=None)
    if not rq.check_user(tg_id=tg_id):
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "Ник отсутствует"
        rq.add_user(tg_id=tg_id, username=username)
        await message.answer("Здравствуйте это тг бот для регистрации, как вас зовут?")
        await state.set_state(Registration.name)
    else:
        user = rq.get_user(tg_id=tg_id)
        await message.reply("Вас приветствует бот!")
        await message.answer(f"Здравствуйте, {user[2]}")


@router.message(F.text, StateFilter(Registration.name))
async def get_name(message: Message, state: FSMContext) -> None:
    """
    РЕГИСТРАЦИЯ - получаем имя пользователя
    :param message:
    :param state:
    :return:
    """
    name, tg_id = message.text, message.chat.id
    rq.set_user_name(tg_id=tg_id, name=name)
    await message.reply('Укажите ваш возраст')
    await state.set_state(Registration.age)


@router.message(F.text, StateFilter(Registration.age))
async def get_name(message: Message, state: FSMContext) -> None:
    """
    РЕГИСТРАЦИЯ - получаем имя пользователя
    :param message:
    :param state:
    :return:
    """
    age_str, tg_id = message.text, message.chat.id
    try:
        age = int(age_str)
        if 0 > age or age > 100:
            await message.answer(text='Не корректно указан возраст. Повторите ввод')
            return
    except:
        await message.answer(text='Введите число')
        return
    today = datetime.datetime.today().strftime("%d/%m/%Y")
    rq.set_user_age(tg_id=tg_id, age=age, data_registration=today)
    await message.reply('Благодарю за регистрацию')
    await state.set_state(state=None)
