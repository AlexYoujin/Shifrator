import re
from datetime import datetime
from typing import Tuple


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
    Извлекает слово перед номерами и все номера из строки.

    Args:
        input_string (str): Входная строка.

    Returns:
        tuple: Пара (слово, строка всех номеров).
    """
    match = re.match(r"(\D+)?([\d\s]+)", input_string)
    if match:
        word = match.group(1).strip() if match.group(1) else ""
        number = re.sub(r"\s", "", match.group(2))  # Убираем пробелы из числовой части
        return word, number
    else:
        return "", input_string


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
        if len(card) != 16 or not card.isdigit():
            raise ValueError("Invalid card number")
        return card[:4] + " " + card[4:6] + "** **** " + card[-4:]

    account_match = re.search(r'Account (\d+)', input_str)
    card_match = re.search(r'Card (\d{4} \d{4} \d{4} \d{4})', input_str)
    raw_card_match = re.search(r'Card (\d+)', input_str)

    if account_match:
        account = account_match.group(1)
        if not account.isdigit():
            raise ValueError("Invalid account number")
        return input_str.replace(account, mask_card(account) if len(account) == 16 else mask_account(account))
    elif card_match:
        card = card_match.group(1).replace(" ", "")
        if not card.isdigit():
            raise ValueError("Invalid card number")
        return input_str.replace(card_match.group(1), mask_card(card))
    elif raw_card_match:
        card = raw_card_match.group(1)
        if not card.isdigit() or len(card) != 16:
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


def main():
    # Пример использования для форматирования даты
    date_user = input("Введите дату платежа (например, '2024-03-11T02:26:18.671407'): ")
    try:
        formatted_date = get_date(date_user)
        print("Форматированная дата:", formatted_date)
    except ValueError as e:
        print(f"Ошибка при обработке даты: {e}")

    while True:
        user_input = input("Введите номер карты или счета (или 'exit' для выхода): ")
        if user_input.lower() == "exit":
            break
        try:
            result = mask_account_card(user_input)
            print("Замаскированные данные:", result)
        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
