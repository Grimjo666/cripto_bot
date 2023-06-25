import requests
import json
import pickle
from datetime import datetime


def get_cripto_info(id: str) -> tuple[str, int, str]:
    """
    Функция принимает ID криптовалюты, делает запрос к API
    и возвращает кортеж (название криптовалюты, цена, дата)
    """
    with open('data/crypto_dict.pkl', 'rb') as file:
        loaded_dict = pickle.load(file)
        for key, value in loaded_dict.items():
            if id in key:
                response = requests.get(f'https://api.coincap.io/v2/assets/{value}')
                cripto_dict = json.loads(response.text)

                dt = datetime.fromtimestamp(cripto_dict['timestamp'] / 1000)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")

                return cripto_dict['data']['name'], cripto_dict['data']['priceUsd'], formatted_time
        else:
            raise ValueError(f"У меня нет информации о криптовалюте: {id}")


# with open('../../data/crypto_dict.pkl', 'wb') as file:
#     response = requests.get('https://api.coincap.io/v2/assets')
#     di = json.loads(response.text)
#     res = {}
#     for item in di['data']:
#         temp = []
#         for key, value in item.items():
#             if key in ('id', 'symbol', 'name'):
#                 temp.append(value.lower())
#         res[tuple(set(temp))] = temp[0]
#     pickle.dump(res, file)








