from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import pickle

from bot import cripto_conversion, bot, conversion_menu, conversion_menu_last
from .cripto_info_handlers import MenuState


# Функция для проверки на корректность вводимых данных пользователем
def check_cripto_info(cripto_info):
    with open('data/crypto_dict.pkl', 'rb') as file:
        loaded_dict = pickle.load(file)
        for key, value in loaded_dict.items():
            if cripto_info[0].lower() in key:
                if len(cripto_info) > 1 and type(cripto_info) is list:
                    return cripto_info[1].isdigit()
                return True
        return False


# Присылаем меню конвертации и просим пользователя ввести название криптовалюты
async def send_conversion_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(message_id=callback_query.message.message_id,
                                chat_id=callback_query.message.chat.id,
                                text='Введите название исходной валюты латиницей, через пробел укажите количество'
                                     ' (если это необходимо)\n'
                                     'Пример: "Bitcoin 10" или "BTC 10"\n',
                                reply_markup=conversion_menu)

    await state.update_data(menu_id=callback_query.message.message_id)
    await MenuState.conversion_menu.set()


# Просим пользователя ввести название валюты, в которую будет конвертироваться предыдущая выбранная валюта
async def send_conversion_menu_next(message: types.Message, state: FSMContext):
    data = await state.get_data()
    menu_id = data.get('menu_id')

    await bot.edit_message_text(message_id=menu_id,
                                chat_id=message.chat.id,
                                text='Введите название целевой валюты латиницей и нажмите\n'
                                     'Пример: "Solana" или "SOL"\n',
                                reply_markup=conversion_menu)

    message_from_user = message.text.split()  # Получаем название первой валюты и количество если указано

    if check_cripto_info(message_from_user):
        await state.update_data(cripto_info=message_from_user)
        await MenuState.conversion_menu_next.set()
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
    else:
        await message.answer(f'Не корректные данные {message_from_user}')


# Получаем название второй валюты и присылаем информацию о конвертации пользователю
async def send_conversion_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    first_cripto, *count = data.get('cripto_info')
    menu_id = data.get('menu_id')

    # Счетчик количества первой валюты
    if not count:
        count = 1
    else:
        count = float(count[0])

    message_from_user = message.text.split()  # Получаем название второй валюты

    if check_cripto_info(message_from_user):
        first_currency, second_currency, price, time = cripto_conversion(first_cripto, message_from_user[0], count)
        await bot.edit_message_text(message_id=menu_id,
                                    chat_id=message.chat.id,
                                    text=f'Конвертируем {first_currency} в {second_currency}\n\n'
                                         f'{second_currency} = {price}$\n\n'
                                         f'Время {time}',
                                    reply_markup=conversion_menu_last)

        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)

    else:
        await message.answer('Не корректные данные ')


def register_conversion_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(send_conversion_menu, lambda c: c.data == 'button_conversion')
    dp.register_message_handler(send_conversion_menu_next, state=MenuState.conversion_menu)
    dp.register_message_handler(send_conversion_info, state=MenuState.conversion_menu_next)
