from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_main_button() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Главное меню')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)
    return keyboard


def main_keyboard(auth: bool) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text="О клане", callback_data='about_clan')
    button_2 = InlineKeyboardButton(text="Правила клана", callback_data='rule_clan')
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


def keyboard_pass_opros(callback: str) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Пропустить', callback_data=callback)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard

