from pathlib import Path
import json
from decorators import log


@log()
def read_transactions(file_path):
    """
    Читает JSON-файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь до JSON-файла.
    :return: Список транзакций или пустой список в случае ошибки.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


# Пример использования функции
"""if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / 'data' / 'operations.json'
    transactions = read_transactions(file_path)
    print(transactions)"""
