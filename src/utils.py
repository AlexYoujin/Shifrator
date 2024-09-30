import json
import pandas as pd
from pathlib import Path
from src.decorators import log

@log("utils")
def read_transactions(file_path):
    """
    Читает файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь до файла (JSON, CSV или XLSX).
    :return: Список транзакций или пустой список в случае ошибки.
    """
    try:
        file_extension = Path(file_path).suffix.lower()

        if file_extension == ".json":
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    return []

        elif file_extension == ".csv":
            df = pd.read_csv(file_path)
            return df.to_dict(orient="records")

        elif file_extension == ".xlsx":
            df = pd.read_excel(file_path)
            return df.to_dict(orient="records")

        else:
            raise ValueError("Unsupported file format")

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except pd.errors.ParserError:
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
