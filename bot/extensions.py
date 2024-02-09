import requests
import json
from config import keys
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base and quote in keys.keys():
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}. Для просмотра доступных валют нажмите на /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Для просмотра доступных валют нажмите на /values')

        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f'Не удалось обработать колличество {amount}. Пожалуйста введите число цифрами')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        status_code = r.status_code
        total_base = json.loads(r.content)[keys[base]] * amount
        return total_base
