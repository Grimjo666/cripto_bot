from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import pickle


# Основные кнопки
button_close = InlineKeyboardButton('❌', callback_data='button_close')
button_main_menu = InlineKeyboardButton('В основное меню', callback_data='button_main_menu')
button_cripto_buttons = InlineKeyboardButton('Список доступных валют', callback_data='button_cripto_buttons')


# Основное меню бота
main_menu = InlineKeyboardMarkup(row_width=1)

button_current_rate = InlineKeyboardButton('Текущий курс', callback_data='button_current_rate')
button_conversion = InlineKeyboardButton('Конвертировать валюту', callback_data='button_conversion')

main_menu.add(button_current_rate, button_conversion, button_close)


# Меню курс сейчас
rate_now_menu = InlineKeyboardMarkup(row_width=1)

rate_now_menu.add(button_cripto_buttons, button_main_menu, button_close)


# Меню конвертации
conversion_menu = InlineKeyboardMarkup(row_width=1)

conversion_menu.add(button_cripto_buttons, button_main_menu, button_close)

conversion_menu_last = InlineKeyboardMarkup()

conversion_menu_last.add(button_main_menu, button_close)


# Клавиатура с названиями криптовалют
cripto_buttons = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)

with open('data/crypto_dict.pkl', 'rb') as file:
    loaded_dict = pickle.load(file)
    for value in loaded_dict.values():
        cripto_buttons.add(KeyboardButton(value.title()))