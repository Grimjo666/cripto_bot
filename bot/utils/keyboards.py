from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import pickle


# Основные кнопки
button_close = InlineKeyboardButton('❌', callback_data='button_close')
button_main_menu = InlineKeyboardButton('В основное меню', callback_data='button_main_menu')
button_cripto_buttons = InlineKeyboardButton('Список доступных валют', callback_data='button_cripto_buttons')


# меню с двумя кнопками в основное меню или закрыть
main_menu_or_close = InlineKeyboardMarkup()

main_menu_or_close.add(button_main_menu, button_close)


# Основное меню бота
main_menu = InlineKeyboardMarkup(row_width=1)

button_current_rate = InlineKeyboardButton('Текущий курс', callback_data='button_current_rate')
button_conversion = InlineKeyboardButton('Конвертировать валюту', callback_data='button_conversion')
button_history_conversion = InlineKeyboardButton('История конвертации', callback_data='button_history_conversion')
button_graphs_menu = InlineKeyboardButton('Графики', callback_data='button_graphs_menu')

main_menu.add(button_current_rate, button_conversion, button_history_conversion, button_graphs_menu, button_close)


# Меню курс сейчас
rate_now_menu = InlineKeyboardMarkup(row_width=1)

rate_now_menu.add(button_cripto_buttons, button_main_menu, button_close)


# Меню конвертации
conversion_menu = InlineKeyboardMarkup(row_width=1)

conversion_menu.add(button_cripto_buttons, button_main_menu, button_close)


# Клавиатура с названиями криптовалют
cripto_buttons = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=False)

with open('data/crypto_dict.pkl', 'rb') as file:
    loaded_dict = pickle.load(file)
    for value in loaded_dict.values():
        cripto_buttons.add(KeyboardButton(value.title()))


# Меню история конвертации
history_conversion_menu = InlineKeyboardMarkup()

history_conversion_menu.add(button_close)


# Меню графиков
graph_menu = InlineKeyboardMarkup(row_width=1)

graph_menu.add(cripto_buttons, button_main_menu, button_close)
