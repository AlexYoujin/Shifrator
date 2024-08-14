import requests


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

    url = f"https://api.apilayer.com/exchangerates_data/convert"
    params = {"from": currency, "to": "RUB", "amount": amount}
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data.get("result", 0.0))
    except requests.RequestException:
        return 0.0
