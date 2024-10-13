from datetime import datetime
from typing import Dict, List

from src.decorators import log
from src.widget import get_date


@log("processing")
def create_payment_dict(payments: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """
    Создает словарь платежей, сгруппированных по дате.

    :param payments: Список платежей, каждый из которых представлен как словарь с ключами "date" и другими данными.
    :return: Словарь, где ключи — это даты, а значения — списки платежей, соответствующих каждой дате.
    """
    payment_dict: Dict[str, List[Dict[str, str]]] = {}
    for payment in payments:
        date = get_date(payment["date"])
        if date not in payment_dict:
            payment_dict[date] = []
        payment_dict[date].append(payment)
    return payment_dict


@log("processing")
def sort_payment_dates(payment_dict: Dict[str, List[Dict[str, str]]]) -> List[str]:
    """
    Сортирует даты в словаре платежей по возрастанию.

    :param payment_dict: Словарь, где ключи — это даты, а значения — списки платежей.
    :return: Отсортированный список дат в формате "дд.мм.гггг".
    """
    sorted_dates = sorted(
        payment_dict.keys(), key=lambda date: datetime.strptime(date, "%d.%m.%Y")
    )
    return sorted_dates
