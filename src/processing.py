from datetime import datetime
from typing import Dict, List

from src.widget import get_date


def create_payment_dict(
    payments: List[Dict[str, str]]
) -> Dict[str, List[Dict[str, str]]]:
    payment_dict: Dict[str, List[Dict[str, str]]] = {}
    for payment in payments:
        date = get_date(payment["date"])
        if date not in payment_dict:
            payment_dict[date] = []
        payment_dict[date].append(payment)
    return payment_dict


def sort_payment_dates(payment_dict: Dict[str, List[Dict[str, str]]]) -> List[str]:
    sorted_dates = sorted(
        payment_dict.keys(), key=lambda date: datetime.strptime(date, "%d.%m.%Y")
    )
    return sorted_dates
