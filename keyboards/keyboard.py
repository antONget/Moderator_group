from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard(auth: bool) -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text="О клане")
    button_2 = KeyboardButton(text="Правила клана")
    button_3 = KeyboardButton(text="Правила пранков")
    button_4 = KeyboardButton(text="Набор в клан")
    button_5 = KeyboardButton(text="Перевод")
    button_6 = KeyboardButton(text="Рейтинг")
    button_7 = KeyboardButton(text="Активности")
    button_8 = KeyboardButton(text="Жалоба")
    button_9 = KeyboardButton(text="Отпуск")
    if not auth:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[button_1], [button_2], [button_3], [button_4]],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[button_1], [button_2], [button_3], [button_5], [button_6], [button_7], [button_8], [button_9]],
            resize_keyboard=True
        )
    return keyboard


def keyboard_pass_opros(callback: str) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Пропустить', callback_data=callback)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard

