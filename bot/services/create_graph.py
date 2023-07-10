import json
import pickle
from datetime import datetime

import requests

end = int(datetime(2023, 7, 6).timestamp()) * 1000
start = int(datetime(2023, 7, 4).timestamp()) * 1000


def get_period_currency_price(currency, start, end):



    with open('../../data/crypto_dict.pkl', 'rb') as file:
        loaded_dict = pickle.load(file)
        for key, value in loaded_dict.items():
            if currency.lower() in key:
                response = requests.get(f"https://api.coincap.io/v2/assets/{value}/history?interval=d1&start={start}&end={end}")
                cripto_dict = json.loads(response.text)

            dt = datetime.fromtimestamp(cripto_dict['timestamp'] / 1000)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")

        return cripto_dict['data'], formatted_time


print(get_period_currency_price('btc', start, end))