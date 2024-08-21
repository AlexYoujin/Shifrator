from decorators import log

@log()
def filter_by_currency(transactions, currency_code):
    """
    Генератор, который возвращает транзакции, где валюта операции соответствует заданной.

    :param transactions: список словарей, представляющих транзакции
    :param currency_code: код валюты (например, "USD")
    :return: итератор, который поочередно выдает транзакции с заданной валютой
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction

@log()
def transaction_descriptions(transactions):
    """
    Генератор, который возвращает описание каждой операции по очереди.

    :param transactions: список словарей, представляющих транзакции
    :return: итератор, который поочередно выдает описание каждой операции
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description

@log()
def card_number_generator(start, end):
    """
    Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне.

    :param start: начальное значение для генерации номеров
    :param end: конечное значение для генерации номеров
    :return: итератор, который поочередно выдает номера карт
    """
    for number in range(start, end + 1):
        card_number = f"{number:016d}"  # Форматируем число с ведущими нулями до 16 цифр
        formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number
