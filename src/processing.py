from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(records: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        records (List[Dict[str, Any]]): Список словарей, каждый из которых представляет запись.
        state (str, optional): Значение ключа 'state', по которому будет фильтрация. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict[str, Any]]: Новый список словарей, содержащий записи, с ключем 'state' соответствует заданному.
    """
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по значению ключа 'date'.

    Args:
        records (List[Dict[str, Any]]): Список словарей, каждый из которых представляет запись.
        reverse (bool, optional): Определяет порядок сортировки. Если True, сортировка по убыванию. По умолчанию True.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список словарей.
    """
    for record in records:
        record["date"] = datetime.strptime(record["date"], "%Y-%m-%dT%H:%M:%S.%f")

    sorted_records = sorted(records, key=lambda x: x["date"], reverse=reverse)

    for record in sorted_records:
        record["date"] = record["date"].strftime("%Y-%m-%dT%H:%M:%S.%f")

    return sorted_records


# Примерные данные для тестирования
records: List[Dict[str, Any]] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Тестирование функции filter_by_state
filtered_records: List[Dict[str, Any]] = filter_by_state(records)
print("Filtered Records:")
for record in filtered_records:
    print(record)

# Ожидаемый результат:
# [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

# Тестирование функции sort_by_date
sorted_records: List[Dict[str, Any]] = sort_by_date(filtered_records)
print("\nSorted Records (Descending):")
for record in sorted_records:
    print(record)

# Ожидаемый результат:
# [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

# Тестирование функции sort_by_date с reverse=False
sorted_records_asc: List[Dict[str, Any]] = sort_by_date(filtered_records, reverse=False)
print("\nSorted Records (Ascending):")
for record in sorted_records_asc:
    print(record)

# Ожидаемый результат:
# [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#  {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
