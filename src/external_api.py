import requests
import os
from decorators import log
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

@log()
def get_api_key():
    """
    Получает API ключ из переменной окружения.

    :return: API ключ как строку.
    """
    return os.getenv("EXCHANGE_RATE_API_KEY")

@log()
def convert_to_rubles(transaction, api_key):
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с информацией о транзакции.
    :param api_key: API ключ для доступа к Exchange Rates Data API.
    :return: Сумма транзакции в рублях (float).
    """
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return float(amount)

    url = "https://api.apilayer.com/exchangerates_data/convert"
    params = {"from": currency, "to": "RUB", "amount": amount}
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        converted_amount = float(data.get("result", 0.0))
        return converted_amount
    except requests.RequestException as e:
        logging.error(f"Ошибка при конвертации валюты: {e}")
        return 0.0

# Пример использования
"""if __name__ == "__main__":
    transaction = {"amount": 100, "currency": "USD"}
    api_key = get_api_key()
    if api_key:
        rub_amount = convert_to_rubles(transaction, api_key)
        print(f"Сумма в рублях: {rub_amount}")
    else:
        print("API ключ не найден.")"""
