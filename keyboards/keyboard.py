from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_main_button() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Главное меню')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)
    return keyboard


def main_keyboard(auth: bool) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text="О клане", url='https://telegra.ph/O-KLANE-12-17')
    button_2 = InlineKeyboardButton(text="Правила клана", url='https://telegra.ph/PRAVILA-KLANA-12-14-3')
    button_3 = InlineKeyboardButton(text="Правила пранков", callback_data='rule_prank')
    button_4 = InlineKeyboardButton(text="Набор в клан", callback_data='recruting_clan')
    button_5 = InlineKeyboardButton(text="Перевод", callback_data='rule_prank')
    button_6 = InlineKeyboardButton(text="Рейтинг", callback_data='honor')
    button_7 = InlineKeyboardButton(text="Активности", callback_data='activity')
    button_8 = InlineKeyboardButton(text="Жалоба", callback_data=' ')
    button_9 = InlineKeyboardButton(text="Отпуск", callback_data=' ')
    if not auth:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_1], [button_2], [button_4]]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_1], [button_2], [button_5], [button_6], [button_7], [button_8], [button_9]]
        )
    return keyboard


def main_keyboard_group() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text="О клане", url='https://telegra.ph/O-KLANE-12-17')
    button_2 = InlineKeyboardButton(text="Правила клана", url='https://telegra.ph/PRAVILA-KLANA-12-14-3')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_pass_opros(callback: str) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Пропустить', callback_data=callback)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_main_admin() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='НАЧАТЬ НАБОР')
    button_2 = KeyboardButton(text='ЗАВЕРШИТЬ НАБОР')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]],
                                   resize_keyboard=True)
    return keyboard


def keyboard_action_recruting(id_recruting: int) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Рассмотреть', callback_data=f'consider_{id_recruting}')
    button_2 = InlineKeyboardButton(text='Отказать', callback_data=f'deny_{id_recruting}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_consider_opros() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Отправить скриншот', callback_data='send_screenshot')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_action_recruting_2(id_recruting: int) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Принять', callback_data=f'accept_{id_recruting}')
    button_2 = InlineKeyboardButton(text='Отказать', callback_data=f'deny_{id_recruting}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_list_group(list_group: list, tg_id_recruting: int) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for group in list_group:
        button = InlineKeyboardButton(text=f'{group.group_title}', callback_data=f'selectclan_{group.group_id}_{tg_id_recruting}')
        inline_keyboard.append([button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard


def keyboard_link_clan(id_clan: int) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Создать ссылку', callback_data=f'link_clan_{id_clan}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_action_recruting_question() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Да', callback_data=f'yes_recruting_clan')
    button_2 = InlineKeyboardButton(text='Нет', callback_data=f'no_recruting_clan')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard