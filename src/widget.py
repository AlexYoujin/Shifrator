import re
from datetime import datetime
from typing import Tuple

from mask import get_mask_account, get_mask_card_number


def extract_digits(input_string: str) -> str:
    """
    Извлекает цифровую часть из строки.

    Args:
        input_string (str): Входная строка.

    Returns:
        str: Цифровая часть строки.
    """
    return re.sub(r"\D", "", input_string)


def extract_word_and_number(input_string: str) -> Tuple[str, str]:
    """
    Извлекает слово перед номером и сам номер из строки.

    Args:
        input_string (str): Входная строка.

    Returns:
        tuple: Пара (слово, номер).
    """
    match = re.match(r"(\D+)?(\d+)", input_string)
    if match:
        word = match.group(1).strip() if match.group(1) else ""
        number = match.group(2)
        return word, number
    else:
        return "", input_string


def mask_account_card(input_string: str) -> str:
    """
    Определяет тип номера и маскирует его соответствующим образом.

    Args:
        input_string (str): Номер банковской карты или счета.

    Returns:
        str: Маскированный номер.
    """
    word, number = extract_word_and_number(input_string)
    length = len(number)

    if length == 16:
        masked_number = get_mask_card_number(number)
    else:
        masked_number = get_mask_account(number)

    return f"{word} {masked_number}".strip()


def get_date(date_user: str) -> str:
    """
    Преобразует дату из формата "YYYY-MM-DDTHH:MM:SS.SSSSSS" в формат "ДД.ММ.ГГГГ".

    Args:
        date_user (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.SSSSSS".

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ".
    """
    # Преобразуем строку даты в объект datetime
    date_obj = datetime.fromisoformat(date_user)

    # Преобразуем дату в нужный формат
    formatted_date = date_obj.strftime("%d.%m.%Y")

    return formatted_date


# Пример использования для форматирования даты
if __name__ == "__main__":
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
