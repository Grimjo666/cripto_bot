import sqlite3


class User:
    def __init__(self, user_id):
        self._user_id = user_id

    def write_conversion_to_db(self, currency_from, currency_to, amount, price):
        conn = sqlite3.connect('crypto_data.db')
        cursor = conn.cursor()

        # Проверка текущего количества записей для данного пользователя
        cursor.execute('SELECT COUNT(*) FROM user_conversion WHERE user_id = ?', (self._user_id,))
        current_count = cursor.fetchone()[0]

        if current_count < 20:
            # Вставка новых записей для данного пользователя
            cursor.execute('INSERT INTO user_conversion (user_id, amount, currency_from, currency_to, price)'
                           ' VALUES (?, ?, ?, ?, ?)', (self._user_id, amount, currency_from, currency_to, price))
        else:
            # Поиск самой старой записи для данного пользователя
            cursor.execute('SELECT id FROM user_conversion WHERE user_id = ?'
                           ' ORDER BY timestamp ASC LIMIT 1', (self._user_id,))
            oldest_id = cursor.fetchone()[0]

            # Обновление самой старой записи
            cursor.execute('UPDATE user_conversion SET amount = ?, currency_from = ?, currency_to = ?, price = ?'
                           ' WHERE id = ?', (amount, currency_from, currency_to, price, oldest_id))

        conn.commit()
        conn.close()

    def get_conversion_from_db(self):
        conn = sqlite3.connect('crypto_data.db')
        cursor = conn.cursor()

        # Поиск истории конвертации
        cursor.execute('SELECT amount, currency_from, currency_to, price, timestamp FROM user_conversion'
                       ' WHERE user_id = ? ', (self._user_id,))

        conversion_data = cursor.fetchall()

        if conversion_data:
            return conversion_data
        else:
            raise ValueError("Нет доступной истории конвертации для данного пользователя.")