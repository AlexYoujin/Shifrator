import re
from typing import List, Dict


def search_operations(operations: List[Dict[str, str]], search_string: str) -> List[Dict[str, str]]:
    """
    Поиск операций по строке поиска.

    Args:
        operations (List[Dict[str, str]]): Список операций.
        search_string (str): Строка поиска.

    Returns:
        List[Dict[str, str]]: Список операций, соответствующих строке поиска.
    """
    filtered_operations = []
    for operation in operations:
        if re.search(search_string, operation['description'], re.IGNORECASE):
            filtered_operations.append(operation)
    return filtered_operations


def categorize_operations(operations: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
    Категоризация операций по списку категорий.

    Args:
        operations (List[Dict[str, str]]): Список операций.
        categories (List[str]): Список категорий операций.

    Returns:
        Dict[str, int]: Словарь, где ключи — это названия категорий, а значения — это количество операций в каждой категории.
    """
    category_count = {category: 0 for category in categories}
    for operation in operations:
        for category in categories:
            if re.search(category, operation['description'], re.IGNORECASE):
                category_count[category] += 1
    return category_count
