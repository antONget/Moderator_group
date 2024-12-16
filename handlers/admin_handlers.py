from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart

from database import requests as rq
from keyboards.keyboard import keyboard_consider_opros, keyboard_action_recruting_2, keyboard_list_group, keyboard_link_clan
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin

import logging

router = Router()
router.message.filter(F.chat.type == "private")


# Определение состояний
class Registration(StatesGroup):
    name = State()
    age = State()


@router.message(F.text == 'НАЧАТЬ НАБОР')
@router.message(F.text == 'ЗАВЕРШИТЬ НАБОР')
async def process_press_start_admin(message: Message, bot: Bot) -> None:
    logging.info('process_press_start_admin')
    if message.text == 'НАЧАТЬ НАБОР':
        data_recruting = {'id': 1, 'is_recruting': 'True'}
        await rq.add_recruting(data=data_recruting)
        await message.answer(text='Набор в кланы открыт')
    elif message.text == 'ЗАВЕРШИТЬ НАБОР':
        data_recruting = {'id': 1, 'is_recruting': 'False'}
        await rq.add_recruting(data=data_recruting)
        await message.answer(text='Набор в кланы закрыт')


@router.callback_query(F.data.startswith('deny_'))
async def process_deny(callback: CallbackQuery, bot: Bot):
    """
    Отказаться от присланной анкеты для вступления в клан
    :param callback:
    :param bot:
    :return:
    """
    logging.info('process_deny')
    answer = callback.data.split('_')[-1]
    recruting_opros = await rq.get_recruting_opros_id(recruting_id=int(answer))
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await bot.edit_message_text(chat_id=recruting_opros.tg_id,
                                text='К сожалению, вы не приняты в клан, попробуйте в следующий раз',
                                message_id=callback.message.message_id,
                                reply_markup=None)
    await callback.answer()


@router.callback_query(F.data.startswith('consider_'))
async def process_consider(callback: CallbackQuery, bot: Bot):
    """
    Принятие анкеты на вступление в клан
    :param callback:
    :param bot:
    :return:
    """
    logging.info('process_consider')
    answer = callback.data.split('_')[-1]
    recruting_opros = await rq.get_recruting_opros_id(recruting_id=int(answer))
    await callback.message.delete()
    await bot.send_message(chat_id=recruting_opros.tg_id,
                           text='Вы приняты в клан, для того, чтобы я вам отправил ссылку на чат клана необходимо'
                                ' сначала сменить никнейм в PUBG MOBILE и добавить приписку клана с уголками: 『BY』\n\n'
                                'Далее отправьте, пожалуйста, скриншот, который подтвердит, что вы сменили никнейм'
                                ' в PUBG MOBILE" (одно изображение)',
                           reply_markup=keyboard_consider_opros())
    await callback.answer()


@router.callback_query(F.data.startswith('accept_'))
async def process_accept(callback: CallbackQuery, bot: Bot):
    """
    Принятие анкеты на вступление в клан
    :param callback:
    :param bot:
    :return:
    """
    logging.info('process_accept')
    answer = callback.data.split('_')[-1]
    recruting_opros = await rq.get_recruting_opros_id(recruting_id=int(answer))
    list_groups = await rq.get_groups()
    await callback.message.edit_text(text='Выберите клан для добавления пользователя',
                                     reply_markup=keyboard_list_group(list_group=list_groups,
                                                                      tg_id_recruting=recruting_opros.tg_id))
    await callback.answer()


@router.callback_query(F.data.startswith('selectclan_'))
async def process_select_clan(callback: CallbackQuery, bot: Bot):
    """
    Принятие анкеты на вступление в клан
    :param callback:
    :param bot:
    :return:
    """
    logging.info('process_accept')
    clan_id = callback.data.split('_')[-2]
    group = await rq.get_groups_group_id(group_id=int(clan_id))
    tg_id_recruting = callback.data.split('_')[-1]
    await bot.send_message(chat_id=tg_id_recruting,
                           text='Вы приняты в клан, для формирования ссылки на чат нажмите на кнопку "Создать ссылку"',
                           reply_markup=keyboard_link_clan(id_clan=int(clan_id)))
    await callback.message.edit_text(text=f'Пользователю отправлено сообщение для добавления в клан {group.group_title}',
                                     reply_markup=None)
    await callback.answer()
