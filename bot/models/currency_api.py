import requests
import json


class CurrencyAPI:
    _link = "https://api.coincap.io/v2/"

    def get_currency_price(self, currency) -> tuple:
        """
        Получаем имя валюты и возвращаем кортеж с данными об этой валюте
        """
        response = requests.get(f'{self._link}assets/{currency}')
        currency_dict = json.loads(response.text)

        return currency_dict['data']['name'], currency_dict['data']['priceUsd'], currency_dict['timestamp']

    def convert_currency(self, currency1, currency2):
        """Получаем имя двух валют и возвращаем кортеж с данными"""
        response = requests.get(f'{self._link}assets?ids={currency1},{currency2}')
        temp = json.loads(response.text)
        currency_dicts = temp['data']

        return currency_dicts[0]['name'], currency_dicts[0]['priceUsd'],\
            currency_dicts[1]['name'], currency_dicts[1]['priceUsd'], temp['timestamp']


test = CurrencyAPI()

# print(test.get_currency_dict('bitcoin'))
print(test.convert_currency('bitcoin', 'ethereum'))