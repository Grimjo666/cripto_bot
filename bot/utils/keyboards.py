from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Основные кнопки
button_close = InlineKeyboardButton('❌', callback_data='button_close')
button_main_menu = InlineKeyboardButton('В основное меню', callback_data='button_main_menu')


# Основное меню бота
main_menu = InlineKeyboardMarkup(row_width=1)

button_current_rate = InlineKeyboardButton('Текущий курс', callback_data='button_current_rate')

main_menu.add(button_current_rate, button_close)


# Меню курс сейчас
rate_now_menu = InlineKeyboardMarkup(row_width=1)

rate_now_menu.add(button_main_menu, button_close)