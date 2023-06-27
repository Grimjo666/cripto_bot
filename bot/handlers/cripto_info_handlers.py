from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot, get_cripto_info, rate_now_menu, cripto_buttons


class MenuState(StatesGroup):
    rate_now_menu = State()
    conversion_menu = State()
    conversion_menu_next = State()


async def send_rate_now_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Присылаем пользователю меню rate_now_menu и ждём от него название криптовалюты
    """
    await bot.edit_message_text(message_id=callback_query.message.message_id,
                                chat_id=callback_query.message.chat.id,
                                text='Введите название нужной вам валюты латиницей\n'
                                     'Пример: "Bitcoin" или "BTC"\n'
                                     'Вы можете указать сразу несколько валют через пробел\n'
                                     'Пример: "BTC SOL ETH"',
                                reply_markup=rate_now_menu)

    await state.update_data(rate_menu_id=callback_query.message.message_id)
    await MenuState.rate_now_menu.set()


# Отправляем пользователю информацию о криптовалютах
async def send_cripto_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('rate_menu_id')
    cripto_id_list = message.text.lower().split()
    counter = len(cripto_id_list)
    text = 'Стоимость валюты высчитывается как средняя стоимость с разных торговых площадок\n\n\n'

    try:
        # Собираем сообщение для пользователя
        for cripto_id in cripto_id_list:
            name, price, time = get_cripto_info(cripto_id)
            text += f'Валюта: {name}\n\n' \
                    f'--Цена: {price}$\n\n' \
                    f'--Время: {time}'

            # Счётчик количества требуемых валют пользователем
            counter -= 1
            if counter != 0:
                text += '\n\n\n'

        await bot.edit_message_text(message_id=message_id,
                                    chat_id=message.chat.id,
                                    text=text,
                                    reply_markup=rate_now_menu)

        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)

    except Exception as ex:
        if type(ex) is ValueError:
            await bot.send_message(chat_id=message.chat.id, text=ex)
        else:
            print(ex)


# Присылаем пользователю клавиатуру с кнопками-названиями валют
async def send_cripto_buttons(callback_query: types.CallbackQuery):

    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text='Выберите криптовалюту:',
                           reply_markup=cripto_buttons)


def register_cripto_info_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(send_rate_now_menu, lambda c: c.data == 'button_current_rate')
    dp.register_message_handler(send_cripto_price, state=MenuState.rate_now_menu)
    dp.register_callback_query_handler(send_cripto_buttons, lambda c: c.data == 'button_cripto_buttons', state='*')
