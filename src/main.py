import json
import csv
import openpyxl
from datetime import datetime
import os
from collections import Counter
from src.models import Product, Category


def load_transactions_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_transactions_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.DictReader(file, delimiter=';'))


def load_transactions_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    return [dict(zip(headers, row)) for row in sheet.iter_rows(min_row=2, values_only=True)]


def load_data_from_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []

    # Проход по категориям в JSON
    for category_data in data:
        category = Category(
            name=category_data['name'],
            description=category_data['description']
        )

        # Проход по продуктам каждой категории
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            category.add_product(product)

        categories.append(category)

    return categories


def filter_transactions_by_status(transactions, status):
    status = status.lower()
    return [
        t for t in transactions
        if t.get('state') and t['state'].lower() == status
    ]


def sort_transactions_by_date(transactions, ascending=True):
    def parse_date(date_str):
        try:
            # Попытка разобрать дату с микросекундами и 'Z' на конце
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            try:
                # Попытка разобрать дату без микросекунд, но с 'Z' на конце
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                # Попытка разобрать дату без микросекунд и без 'Z'
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

    return sorted(transactions, key=lambda x: parse_date(x['date']), reverse=not ascending)


def filter_ruble_transactions(transactions):
    return [t for t in transactions if t.get('currency_name') == 'руб.']


def filter_transactions_by_description(transactions, keyword):
    return [t for t in transactions if keyword.lower() in t.get('description', '').lower()]


def get_files_in_directory(directory, extensions):
    return [file for file in os.listdir(directory) if file.endswith(tuple(extensions))]


def get_transaction_amount_and_currency(transaction):
    if 'operationAmount' in transaction:  # JSON format
        return transaction['operationAmount']['amount'], transaction['operationAmount']['currency']['name']
    else:  # CSV/XLSX format
        return transaction['amount'], transaction.get('currency_name', '')


def count_transactions_by_status(transactions):
    statuses = [t.get('state', '').lower() for t in transactions if t.get('state')]
    return Counter(statuses)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Введите номер пункта меню: ")
    data_directory = r"C:\Users\alexy\PycharmProjects\Shifrator\data"
    file_types = {'1': ['.json'], '2': ['.csv'], '3': ['.xlsx']}

    if choice in file_types:
        files = get_files_in_directory(data_directory, file_types[choice])
        if not files:
            print(f"Не найдено файлов с расширением {file_types[choice][0]}")
            return
        print(f"Доступные файлы ({file_types[choice][0]}):")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        file_choice = int(input("Введите номер файла: ")) - 1
        if not (0 <= file_choice < len(files)):
            print("Неверный выбор файла.")
            return
        file_path = os.path.join(data_directory, files[file_choice])

        # Загрузка транзакций в зависимости от выбора
        if choice == '1':
            transactions = load_transactions_from_json(file_path)
        elif choice == '2':
            transactions = load_transactions_from_csv(file_path)
        else:
            transactions = load_transactions_from_xlsx(file_path)

        print(f"Файл {files[file_choice]} успешно загружен.")
    else:
        print("Неверный выбор. Пожалуйста, выберите правильный пункт меню.")
        return

    # Подсчет количества транзакций по статусам
    status_counts = count_transactions_by_status(transactions)
    print("Количество транзакций по статусам:")
    for status, count in status_counts.items():
        print(f"{status}: {count}")

    available_statuses = ["executed", "canceled", "pending"]
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    for i, status in enumerate(available_statuses, start=1):
        print(f"{i}. {status.upper()}")

    status_choice = int(input("Введите номер статуса: ")) - 1
    if not (0 <= status_choice < len(available_statuses)):
        print("Неверный выбор статуса.")
        return

    status = available_statuses[status_choice]
    filtered_transactions = filter_transactions_by_status(transactions, status)
    print(f"Операции отфильтрованы по статусу \"{status.upper()}\"")

    if input("Отсортировать операции по дате? Да/Нет: ").lower() == 'да':
        sort_order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        ascending = sort_order == 'по возрастанию'
        filtered_transactions = sort_transactions_by_date(filtered_transactions, ascending=ascending)

    if input("Выводить только рублевые транзакции? Да/Нет: ").lower() == 'да':
        filtered_transactions = filter_ruble_transactions(filtered_transactions)

    if input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower() == 'да':
        keyword = input("Введите слово для фильтрации: ")
        filtered_transactions = filter_transactions_by_description(filtered_transactions, keyword)

    print("Распечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print(f"Дата: {transaction['date']}")
            print(f"Описание: {transaction['description']}")
            from_account = transaction.get('from', 'Отправитель не указан')
            to_account = transaction.get('to', 'Получатель не указан')
            amount, currency = get_transaction_amount_and_currency(transaction)
            print(f"{from_account} -> {to_account}")
            print(f"Сумма: {amount} {currency}")
            print("-----------")


if __name__ == "__main__":
    main()
