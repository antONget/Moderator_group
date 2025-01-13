import asyncio
import datetime

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto, ChatInviteLink
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter

from database import requests as rq
from keyboards.keyboard import main_keyboard, keyboard_main_admin, keyboard_action_recruting,\
    keyboard_action_recruting_2, keyboard_action_recruting_question
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin
from config_data.config import load_config, Config

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()


# Определение состояний
class Registration(StatesGroup):
    name = State()
    age = State()


class Recruting(StatesGroup):
    opros_1 = State()
    opros_2 = State()
    opros_3 = State()
    opros_4 = State()
    opros_5 = State()
    opros_6 = State()
    opros_7 = State()


@router.message(CommandStart())
@router.message(F.text == 'Главное меню')
@router.message(F.text == '/get_dbfile')
@error_handler
async def process_press_start(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обработка команды /start и 'Главное меню'
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_press_start ')
    await state.set_state(state=None)
    if message.photo:
        print(message.photo[-1].file_id)
        return
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

    # получаем список групп
    groups = await rq.get_groups()
    # флаг того что пользователь состоит в группе
    auth = False
    for group in groups:

        member = await bot.get_chat_member(user_id=message.from_user.id,
                                           chat_id=group.group_id)
        if member.status not in ['left', 'kicked', 'restricted']:
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

    admin = await check_super_admin(telegram_id=message.from_user.id)
    if admin:
        await message.answer(text='Выберите пункт',
                             reply_markup=keyboard_main_admin())


@router.callback_query(F.data == 'recruting_clan')
async def recruting_clan(callback: CallbackQuery, state: FSMContext):
    logging.info(f'recruting_clan {callback.data}')
    await callback.answer()
    recruting_opros = await rq.get_recruting_opros_tg_id(tg_id=callback.from_user.id)
    if recruting_opros:
        date_format = '%d-%m-%Y %H:%M'
        current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
        delta_time = (datetime.datetime.strptime(current_date, date_format) - datetime.datetime.strptime(
            recruting_opros.data_opros,
            date_format))
        if delta_time.days < 7:
            await callback.message.answer(
                text='На текущий момент набор в клан закрыт.',
                reply_markup=None)
            return
    await callback.message.answer(text='У вас есть карта смены ника?',
                                  reply_markup=keyboard_action_recruting_question())


@router.callback_query(F.data == 'no_recruting_clan')
async def no_recruting_clan(callback: CallbackQuery, state: FSMContext):
    logging.info(f'no_recruting_clan  {callback.data}')
    await callback.message.delete()
    await callback.answer()
    recruting_opros = await rq.get_recruting_opros_tg_id(tg_id=callback.from_user.id)
    if recruting_opros:
        date_format = '%d-%m-%Y %H:%M'
        current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
        delta_time = (datetime.datetime.strptime(current_date, date_format) - datetime.datetime.strptime(
            recruting_opros.data_opros,
            date_format))
        if delta_time.days < 7:
            await callback.message.answer(text='К сожалению, для набора в клан необходима карта смены ника в PUBG MOBILE.',
                                          reply_markup=None)
        else:
            data_opros = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
            data_recruting_opros = {'age_opros': 'default',
                                    'tg_id': callback.from_user.id,
                                    'ID_PUBG_MOBILE': 'default',
                                    'kd_Metro_Royale': 'default',
                                    'img_PUBG_MOBILE': 'default',
                                    'img_PUBG_Metro_Royale': 'default',
                                    'about_me': 'default',
                                    'data_opros': data_opros}
            await rq.add_recruting_opros(data=data_recruting_opros)
            await callback.message.answer(text='К сожалению, для набора в клан необходима карта смены ника в PUBG MOBILE.')
    else:
        data_opros = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
        data_recruting_opros = {'age_opros': 'default',
                                'tg_id': callback.from_user.id,
                                'ID_PUBG_MOBILE': 'default',
                                'kd_Metro_Royale': 'default',
                                'img_PUBG_MOBILE': 'default',
                                'img_PUBG_Metro_Royale': 'default',
                                'about_me': 'default',
                                'data_opros': data_opros}
        await rq.add_recruting_opros(data=data_recruting_opros)
        await callback.message.answer(text='К сожалению, для набора в клан необходима карта смены ника в PUBG MOBILE.')


@router.callback_query(F.data == 'yes_recruting_clan')
async def yes_recruting_clan(callback: CallbackQuery, state: FSMContext):
    logging.info(f'yes_recruting_clan  {callback.data}')
    await callback.message.delete()
    recruting = await rq.get_recruting()
    if not recruting:
        return
    msg = ''
    if recruting.is_recruting == 'True':
        recruting_opros = await rq.get_recruting_opros_tg_id(tg_id=callback.from_user.id)
        print(recruting_opros)
        if recruting_opros:
            date_format = '%d-%m-%Y %H:%M'
            current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
            delta_time = (datetime.datetime.strptime(current_date, date_format) - datetime.datetime.strptime(recruting_opros.data_opros,
                                                                                           date_format))
            print(delta_time.days)
            if delta_time.days < 7:
                await callback.message.answer(text='На текущий момент набор в клан закрыт.',
                                              reply_markup=None)
            else:
                msg = await callback.message.edit_text(text='1. Отправьте ваш ID аккаунта из PUBG MOBILE.',
                                                       reply_markup=None)
                await state.set_state(state=Recruting.opros_1)
        else:
            msg = await callback.message.answer(text='1. Отправьте ваш ID аккаунта из PUBG MOBILE.',
                                                   reply_markup=None)
            await state.set_state(state=Recruting.opros_1)
    elif recruting.is_recruting == 'False':
        await callback.message.answer(text='На текущий момент набор в клан закрыт.',
                                         reply_markup=None)
    await state.update_data(msg=msg)
    await callback.answer()


@router.message(F.text, StateFilter(Recruting.opros_1))
async def recruting_opros_1(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_1')
    try:
        opros_1 = int(message.text)
    except:
        await message.answer(text='Пришлите только число')
        await message.delete()
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id+1)
        return
    await message.delete()
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=data['msg'].message_id)
    await state.update_data(opros_1=opros_1)
    msg = await message.answer(text='Сколько вам лет?')
    await state.update_data(msg=msg)
    await state.set_state(state=Recruting.opros_2)


@router.message(F.text, StateFilter(Recruting.opros_2))
async def recruting_opros_2(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_2')
    try:
        opros_2 = int(message.text)
    except:
        await message.answer(text='Пришлите только число')
        await message.delete()
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id + 1)
        return
    await message.delete()
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=data['msg'].message_id)
    await state.update_data(opros_2=opros_2)
    msg = await message.answer(text='3. Какой ваш средний кд в Metro Royale?')
    await state.update_data(msg=msg)
    await state.set_state(state=Recruting.opros_3)


@router.message(F.text, StateFilter(Recruting.opros_3))
async def recruting_opros_3(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_3')
    try:
        opros_3 = float(message.text)
    except:
        await message.answer(text='Пришлите только число')
        await message.delete()
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id + 1)
        return
    await message.delete()
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=data['msg'].message_id)
    await state.update_data(opros_3=message.text)
    msg = await message.answer_photo(photo='AgACAgIAAxkBAAIXf2dhjjHqtgJRVAFRJc7_yI8f-5TVAALw8DEbtbMRSymHzvXTnL7OAQADAgADeQADNgQ',
                                     caption='4. Отправьте скриншот из PUBG MOBILE, где в классическом меню видно информацию'
                                             ' об аккаунте,  уровень, никнейм.\n\nПример на скриншоте')
    await state.update_data(msg=msg)
    await state.set_state(state=Recruting.opros_4)


@router.message(StateFilter(Recruting.opros_4))
async def recruting_opros_4(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_4')
    if message.photo:
        await message.delete()
        data = await state.get_data()
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=data['msg'].message_id)
        file_id = message.photo[-1].file_id
        await state.update_data(opros_4=file_id)
        msg = await message.answer_photo(photo='AgACAgIAAxkBAAIXoGdhkLDedYXeeldmLLQncCzypGQXAAL-8DEbtbMRS4xhfOfp0G5bAQADAgADeQADNgQ',
                                         caption='5. Отправьте скриншот из PUBG Metro Royale, где видно ваш текущий кд, ваш ранг.\n\nПример на скриншоте')
        await state.update_data(msg=msg)
        await state.set_state(state=Recruting.opros_5)
    else:
        msg = await message.answer(text='Пришлите фото')
        await message.delete()
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=msg.message_id)


@router.message(StateFilter(Recruting.opros_5))
async def recruting_opros_5(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_5')
    if message.photo:
        await message.delete()
        data = await state.get_data()
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=data['msg'].message_id)
        file_id = message.photo[-1].file_id
        await state.update_data(opros_5=file_id)
        msg = await message.answer(text='6. Расскажите немного о себе до 300 символов.')
        await state.update_data(msg=msg)
        await state.set_state(state=Recruting.opros_6)
    else:
        msg = await message.answer(text='Пришлите фото')
        await message.delete()
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=msg.message_id)


@router.message(F.text, StateFilter(Recruting.opros_6))
async def recruting_opros_6(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_6')
    await message.delete()
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=data['msg'].message_id)
    await state.set_state(state=None)
    data = await state.get_data()
    data_opros = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    data_recruting_opros = {'age_opros': data['opros_2'],
                            'tg_id': message.from_user.id,
                            'ID_PUBG_MOBILE': data['opros_1'],
                            'kd_Metro_Royale': data['opros_3'],
                            'img_PUBG_MOBILE': data['opros_4'],
                            'img_PUBG_Metro_Royale': data['opros_5'],
                            'about_me': message.text,
                            'data_opros': data_opros}
    await rq.add_recruting_opros(data=data_recruting_opros)
    recruting_opros = await rq.get_recruting_opros_tg_id(tg_id=message.from_user.id)
    await message.answer(text='Ожидайте, пожалуйста, рассмотрения заявки, рекомендуем включить'
                              ' уведомления в данном боте')
    caption = f'<b>Анкета № {recruting_opros.id} от: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a></b>\n'\
              f'<b>ID PUBG MOBILE:</b> {data["opros_1"]}\n' \
              f'<b>Возраст:</b> {data["opros_2"]}\n' \
              f'<b>Средний КД:</b> {data["opros_3"]}\n' \
              f'<b>О себе:</b> {message.text}'
    media_group = []
    i = 0
    for photo in [data['opros_4'], data['opros_5']]:
        i += 1
        if i == 1:
            media_group.append(InputMediaPhoto(media=photo, caption=caption))
        else:
            media_group.append(InputMediaPhoto(media=photo))
    list_admins = config.tg_bot.admin_ids.split(',')
    opros_recruting = await rq.get_recruting_opros()
    for admin in list_admins:
        try:
            await bot.send_media_group(chat_id=admin,
                                       media=media_group)
            await bot.send_message(chat_id=admin,
                                   text=f'№ {recruting_opros.id} выберите действие',
                                   reply_markup=keyboard_action_recruting(id_recruting=opros_recruting.id))
        except:
            pass


@router.callback_query(F.data == 'send_screenshot')
async def recruting_send_screenshot(callback: CallbackQuery, state: FSMContext):
    logging.info(f'recruting_send_screenshot  {callback.data}')
    await callback.answer()
    await callback.message.answer(text='Отправьте скриншот',
                                  reply_markup=None)
    await state.set_state(state=Recruting.opros_7)


@router.message(StateFilter(Recruting.opros_7))
async def recruting_opros_7(message: Message, state: FSMContext, bot: Bot):
    logging.info('recruting_opros_7')
    if message.photo:
        await state.set_state(state=None)
        await message.answer(text='Ожидайте...')
        await message.delete()
        file_id = message.photo[-1].file_id
        recruting_opros = await rq.get_recruting_opros_tg_id(tg_id=message.from_user.id)
        caption = f'<b>Анкета № {recruting_opros.id} от: <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a></b>\n' \
                  f'<b>ID PUBG MOBILE:</b> {recruting_opros.ID_PUBG_MOBILE}\n' \
                  f'<b>Возраст:</b> {recruting_opros.age_opros}\n' \
                  f'<b>Средний КД:</b> {recruting_opros.kd_Metro_Royale}\n' \
                  f'<b>О себе:</b> {recruting_opros.about_me}'
        media_group = []
        i = 0
        for photo in [recruting_opros.img_PUBG_Metro_Royale, recruting_opros.img_PUBG_MOBILE, file_id]:
            i += 1
            if i == 1:
                media_group.append(InputMediaPhoto(media=photo, caption=caption))
            else:
                media_group.append(InputMediaPhoto(media=photo))
        list_admins = config.tg_bot.admin_ids.split(',')
        opros_recruting = await rq.get_recruting_opros_tg_id(tg_id=message.from_user.id)
        for admin in list_admins:
            try:
                await bot.send_media_group(chat_id=admin,
                                           media=media_group)
                await bot.send_message(chat_id=admin,
                                       text=f'№ {recruting_opros.id} выберите действие',
                                       reply_markup=keyboard_action_recruting_2(id_recruting=opros_recruting.id))
            except:
                pass
    else:
        await message.answer(text='Пришлите фото')
        return


@router.callback_query(F.data.startswith('link_clan_'))
async def recruting_send_screenshot(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'recruting_send_screenshot  {callback.data}')
    answer = callback.data.split('_')[-1]
    group = await rq.get_groups_group_id(group_id=int(answer))
    recruting = await rq.get_recruting()
    if recruting.is_recruting == 'True':
        expire_date = datetime.datetime.now() + datetime.timedelta(minutes=10)  # время истечения
        invite_link: ChatInviteLink = await bot.create_chat_invite_link(
            chat_id=int(answer),
            name=f"Одноразовая ссылка для клана - {group.group_title}",
            member_limit=1,
            expire_date=expire_date
        )
        await callback.message.edit_text(text=f'Ссылка для доступа к клану {group.group_title} - {invite_link.invite_link}',
                                         reply_markup=None)
        await rq.update_clan_name(tg_id=callback.from_user.id,
                                  clan_name=group.group_title,
                                  username=callback.from_user.username if callback.from_user.username else 'username')
        await rq.update_data_registration(tg_id=callback.from_user.id)
    else:
        await callback.message.answer(text='К сожалению, набор уже завершен')
    await callback.answer()

