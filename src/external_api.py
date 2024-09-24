import logging
import os

import requests
from dotenv import load_dotenv

from src.decorators import log

# Загрузка переменных окружения из .env файла
load_dotenv()


@log("external_api")
def get_api_key() -> str:
    """
    Получает API ключ из переменной окружения.

    :return: API ключ как строку.
    """
    return os.getenv("EXCHANGE_RATE_API_KEY")


@log("external_api")
def convert_to_rubles(transaction: dict, api_key: str) -> float:
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
