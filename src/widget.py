import re
from datetime import datetime
from typing import Tuple

from decorators import log
from generators import (card_number_generator, filter_by_currency,
                        transaction_descriptions)


@log()
def my_function(x, y):
    return x + y


# Вызов функции
my_function(1, 2)


def extract_digits(input_string: str) -> str:
    """
    Извлекает цифровую часть из строки.

    Args:
        input_string (str): Входная строка.

    Returns:
        str: Цифровая часть строки.
    """
    return re.sub(r"\D", "", input_string)


def extract_word_and_numbers(input_string: str) -> Tuple[str, str]:
    """
    Извлекает первое слово и все номера из строки.

    Args:
        input_string (str): Входная строка.

    Returns:
        tuple: Пара (слово, строка всех номеров).
    """
    # Найти первую последовательность букв
    word_match = re.search(r"[a-zA-Z]+", input_string)
    word = word_match.group(0) if word_match else ""

    # Найти все числа и объединить их в одну строку
    numbers = "".join(re.findall(r"\d+", input_string))

    return word, numbers


def mask_account_card(input_str):
    """
    Определяет тип номера и маскирует его соответствующим образом.

    Args:
        input_string (str): Номер банковской карты или счета.

    Returns:
        str: Маскированный номер.

    Raises:
        ValueError: Если входная строка не является числовой или слишком короткой.
    """

    def mask_account(account):
        if len(account) < 5 or not account.isdigit():
            raise ValueError("Invalid account number")
        return "*" * (len(account) - 4) + account[-4:]

    def mask_card(card):
        if len(card) != 16:
            raise ValueError("Invalid card number")
        return card[:4] + " " + card[4:6] + "** **** " + card[-4:]

    account_match = re.search(r"Account (\d+)", input_str)
    card_match = re.search(r"Card (\d{4} \d{4} \d{4} \d{4})", input_str)
    raw_card_match = re.search(r"Card (\d+)", input_str)

    if account_match:
        account = account_match.group(1)
        if not account.isdigit():
            raise ValueError("Invalid account number")
        return input_str.replace(
            account, mask_card(account) if len(account) == 16 else mask_account(account)
        )
    elif card_match:
        card = card_match.group(1).replace(" ", "")
        if not card.isdigit():
            raise ValueError("Invalid card number")
        return input_str.replace(card_match.group(1), mask_card(card))
    elif raw_card_match:
        card = raw_card_match.group(1)
        if len(card) != 16:
            raise ValueError("Invalid card number")
        return input_str.replace(card, mask_card(card))
    elif input_str.isdigit():
        if len(input_str) == 16:
            return mask_card(input_str)
        elif len(input_str) >= 5:
            return mask_account(input_str)
        else:
            raise ValueError("Invalid input")
    else:
        raise ValueError("Invalid input")


def get_date(date_user: str) -> str:
    """
    Преобразует дату из формата "YYYY-MM-DDTHH:MM:SS.SSSSSS" в формат "ДД.ММ.ГГГГ".

    Args:
        date_user (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.SSSSSS".

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ".
    """
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$")
    if not date_pattern.match(date_user):
        raise ValueError("Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'")

    try:
        date_obj = datetime.fromisoformat(date_user)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date")


# Пример использования filter_by_currency
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 791923212,
        "state": "EXECUTED",
        "date": "2019-06-08T16:32:22.850589",
        "operationAmount": {
            "amount": "10451.88",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        },
        "description": "Перевод с карты на карту",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }
]

# Использование filter_by_currency
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

# Использование transaction_descriptions
descriptions = transaction_descriptions(transactions)
for _ in range(3):
    print(next(descriptions))

# Использование card_number_generator
for card_number in card_number_generator(1, 5):
    print(card_number)


def main():
    date_user = input("Введите дату платежа (например, '2024-03-11T02:26:18.671407'): ")
    try:
        formatted_date = get_date(date_user)
        print(f"Форматированная дата: {formatted_date}")
    except ValueError as e:
        print(f"Ошибка при обработке даты: {e}")

    while True:
        user_input = input("Введите номер карты или счета (или 'exit' для выхода): ")
        if user_input.lower() == "exit":
            break
        try:
            result = mask_account_card(user_input)
            print(f"Замаскированные данные: {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
