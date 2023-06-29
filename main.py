import logging
import os
from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from bot import dp, bot
from bot.utils import main_menu
from bot.handlers import cripto_info_handlers, conversion_handlers


logging.basicConfig(level=logging.INFO)


# Проверка наличия файла базы данных
if not os.path.exists('data/crypto_data.db'):
    # Запуск create_db.py, если файл базы данных отсутствует
    os.system('python data/create_db.py')


cripto_info_handlers.register_cripto_info_handlers(dp)
conversion_handlers.register_conversion_handlers(dp)


@dp.message_handler(commands=['start', 'menu'])
async def command_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Я бот, созданный для получения информации о ценах на крипто-валюты',
                           reply_markup=main_menu)


# присылает main_menu по нажатию на кнопку
@dp.callback_query_handler(lambda c: c.data == 'button_main_menu', state='*')
async def send_main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text='Я бот, созданный для получения информации о ценах на крипто-валюты',
                                reply_markup=main_menu)

    await state.finish()


# Хэндлер для закрытия меню
@dp.callback_query_handler(lambda c: c.data == 'button_close', state='*')
async def close_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
