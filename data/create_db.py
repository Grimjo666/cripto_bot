import sqlite3

# Установка соединения с базой данных
conn = sqlite3.connect('data/crypto_data.db')
cursor = conn.cursor()

# Создание таблицы user_conversion, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS user_conversion (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    amount FLOAT,
                    currency_from TEXT,
                    currency_to TEXT,
                    price FLOAT,   
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

# Фиксация изменений и закрытие соединения
conn.commit()
conn.close()