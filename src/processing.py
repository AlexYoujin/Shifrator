from datetime import datetime
from typing import Dict, List


def get_date(date_user: str) -> str:
    import re

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$")
    if not date_pattern.match(date_user):
        raise ValueError("Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'")

    try:
        date_obj = datetime.fromisoformat(date_user)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date")


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
