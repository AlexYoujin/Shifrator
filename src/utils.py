import json
from pathlib import Path

from src.decorators import log


@log("utils")
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
