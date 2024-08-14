import json
import os


def read_transactions(file_path):
    """
    Читает JSON-файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь до JSON-файла.
    :return: Список транзакций или пустой список в случае ошибки.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, IOError):
        pass

    return []
