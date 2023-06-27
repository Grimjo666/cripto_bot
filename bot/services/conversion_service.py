from .currency_service import get_cripto_info


def cripto_conversion(id1, id2, count=1):
    """Функция для конвертации валют.
    на вход подаётся ИД исходной валюты, целевой валюты и по желанию количество исходной валюты"""
    first_data = get_cripto_info(id1)
    second_data = get_cripto_info(id2)

    price = (float(first_data[1]) / float(second_data[1])) * count

    return first_data[0], second_data[0], price, second_data[-1]
