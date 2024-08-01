import re
from datetime import datetime
from typing import Tuple

from src.mask import get_mask_account, get_mask_card_number


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
    match = re.match(r"(\D+)?(.+)", input_string)
    if match:
        word = match.group(1).strip() if match.group(1) else ""
        numbers = re.sub(r"\D", "", match.group(2))  # Убираем всё нецифровое
        return word, numbers
    else:
        return "", re.sub(r"\D", "", input_string)


def mask_account_card(input_string: str) -> str:
    """
    Определяет тип номера и маскирует его соответствующим образом.

    Args:
        input_string (str): Номер банковской карты или счета.

    Returns:
        str: Маскированный номер.

    Raises:
        ValueError: Если входная строка не является числовой или слишком короткой.
    """
    word, number = extract_word_and_numbers(input_string)
    length = len(number)

    if not number.isdigit():
        raise ValueError("Invalid input, expected a string of digits")

    if length == 16:
        masked_number = get_mask_card_number(number)
    elif length >= 5:
        masked_number = get_mask_account(number)
    else:
        raise ValueError("Number is too short")

    return f"{word} {masked_number}".strip()


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
