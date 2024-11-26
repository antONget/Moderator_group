import logging

from aiogram import Router, F, Bot
from database import requests as rq
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatInviteLink
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter

from keyboards.keyboard import keyboard_main_button
from keyboards.keyboard import keyboard_pass_opros
from utils.error_handling import error_handler


router = Router()
router.message.filter(F.chat.type == "private")


class Registration(StatesGroup):
    year = State()
    name = State()
    number = State()
    nickname = State()


@router.message(Command('opros'))
@error_handler
async def into_command_opros(message: Message, state: FSMContext, bot: Bot):
    groups = await rq.get_groups()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id) #Удаление сообщения
    for group in groups:
        member = await bot.get_chat_member(user_id=message.from_user.id,
                                        chat_id=group.group_id)
        if member.status != 'left':
            break
    else:
        await message.answer('Вас нет в тг группах')
        return
    logging.info('into_command_opros')
    user = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if not user.age:
        await message.answer("Сколько вам лет? (принимаются только цифры)")
    else:
        await message.answer(
            " Сколько вам лет? (принимаются только цифры)",
            reply_markup=keyboard_pass_opros(callback='button1')
        )
    await state.set_state(Registration.year)


@router.callback_query(F.data.in_({"button1", "button2", "button3", "button4"}))
@error_handler
async def process_multiple_callbacks(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info('process_multiple_callbacks')
    if callback.data == "button1":
        await state.set_state(Registration.year)
    elif callback.data == "button2":
        await state.set_state(Registration.name)
    elif callback.data == "button3":
        await state.set_state(Registration.number)
    elif callback.data == "button4":
        await state.set_state(Registration.nickname)


# Шаг 1: Получение года рождения
@router.message(F.text, StateFilter(Registration.year))
@error_handler
async def get_age(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_age')
    # Проверяем, что введено число
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст.")
        return
    try:
        age = int(message.text)
    except:
        await message.answer(text='Пожалуйста, введите корректный возраст.')
        return

    await rq.update_user_age(age=age, tg_id=message.from_user.id)
    user = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if not user.name:
        await message.answer("Введите ваше имя:")
    else:
        await message.answer("Введите ваше имя:",
                             reply_markup=keyboard_pass_opros(callback='button2'))
    await state.set_state(Registration.name)  # Переходим к состоянию name


# Шаг 2: Получение имени
@router.message(F.text, StateFilter(Registration.name))
@error_handler
async def get_name(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_name')
    await rq.update_user_name(tg_id=message.from_user.id, name=message.text)
    user = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if not user.id_PUBG_MOBILE:
        await message.answer("Введите ваш ID в PUBG_MOBILE:")
    else:
        await message.answer("Введите ваш ID в PUBG_MOBILE:",
                             reply_markup=keyboard_pass_opros(callback='button3'))
    await state.set_state(Registration.number)  # Переход к состоянию number


# Шаг 3: Получение ID
@router.message(F.text, StateFilter(Registration.number))
@error_handler
async def get_number(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_number')
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите ID из PUBG MOBILE.")
        return
    await rq.update_user_id_pubg(tg_id=message.from_user.id, id_pubg=int(message.text))
    user = await rq.get_user_tg_id(tg_id=message.from_user.id)
    if not user.nickname:
        await message.answer("Введите ваш никнейм в PUBG MOBILE:")
    else:
        await message.answer("Введите ваш никнейм в PUBG MOBILE:",
                             reply_markup=keyboard_pass_opros(callback='button4'))
    await state.set_state(Registration.nickname)  # Переход к состоянию nickname


# Шаг 4: Получение никнейма и завершение регистрации
@router.message(F.text, StateFilter(Registration.nickname))
@error_handler
async def get_nickname(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_nickname')
    await rq.update_user_nickname(tg_id=message.from_user.id, nickname=message.text)
    general_group = await rq.get_groups_general()
    member = await bot.get_chat_member(user_id=message.from_user.id, chat_id=general_group.group_id)
    if member.status == 'left':
        invite_link: ChatInviteLink = await bot.create_chat_invite_link(
                chat_id=general_group.group_id,
                name="Одноразовая ссылка",
                member_limit=1  # Ограничение: 1 пользователь
            )
        await message.answer(text=f'Вы прошли регистрацию, вот ссылка на группу:'
                                  f' <a href="{invite_link.invite_link}">общая группа</a>',
                             parse_mode="HTML", reply_markup=keyboard_main_button())
        await rq.update_invitation(tg_id=message.from_user.id, invitation=invite_link)
    else:
        await message.answer("Вы обновили свои данные")
    await state.set_state(state=None)
