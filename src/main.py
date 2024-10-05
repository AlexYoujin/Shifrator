import json
import csv
import openpyxl
from datetime import datetime
import os


def load_transactions_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transactions = json.load(file)
    return transactions


def load_transactions_from_csv(file_path):
    transactions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            transactions.append(row)
    return transactions


def load_transactions_from_xlsx(file_path):
    transactions = []
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        transaction = dict(zip(headers, row))
        transactions.append(transaction)
    return transactions


def filter_transactions_by_status(transactions, status):
    status = status.lower()
    filtered_transactions = [
        t for t in transactions
        if 'state' in t and t['state'] is not None and t['state'].lower() == status
    ]
    return filtered_transactions


def sort_transactions_by_date(transactions, ascending=True):
    return sorted(transactions, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                  reverse=not ascending)


def filter_ruble_transactions(transactions):
    return [t for t in transactions if 'currency_name' in t and t['currency_name'] == 'руб.']


def filter_transactions_by_description(transactions, keyword):
    return [t for t in transactions if 'description' in t and keyword.lower() in t['description'].lower()]


def get_files_in_directory(directory, extensions):
    """
    Получает список файлов с заданными расширениями в указанной директории.

    Args:
        directory (str): Путь к директории.
        extensions (list): Список расширений файлов.

    Returns:
        list: Список файлов с заданными расширениями.
    """
    files = []
    for file in os.listdir(directory):
        if file.endswith(tuple(extensions)):
            files.append(file)
    return files


def get_transaction_amount_and_currency(transaction):
    """Получает сумму и валюту в зависимости от формата данных."""
    if 'operationAmount' in transaction:
        # JSON формат
        return transaction['operationAmount']['amount'], transaction['operationAmount']['currency']['name']
    else:
        # CSV/XLSX формат
        return transaction['amount'], transaction.get('currency_name', '')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Введите номер пункта меню: ")
    data_directory = r"C:\Users\alexy\PycharmProjects\Shifrator\data"
    if choice == '1':
        files = get_files_in_directory(data_directory, ['.json'])
        if not files:
            print("Не найдено ни одного JSON-файла в директории.")
            return
        print("Доступные JSON-файлы:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        file_choice = int(input("Введите номер файла: ")) - 1
        if file_choice < 0 or file_choice >= len(files):
            print("Неверный выбор файла.")
            return
        file_path = os.path.join(data_directory, files[file_choice])
        transactions = load_transactions_from_json(file_path)
        print("Для обработки выбран JSON-файл.")
    elif choice == '2':
        files = get_files_in_directory(data_directory, ['.csv'])
        if not files:
            print("Не найдено ни одного CSV-файла в директории.")
            return
        print("Доступные CSV-файлы:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        file_choice = int(input("Введите номер файла: ")) - 1
        if file_choice < 0 or file_choice >= len(files):
            print("Неверный выбор файла.")
            return
        file_path = os.path.join(data_directory, files[file_choice])
        transactions = load_transactions_from_csv(file_path)
        print("Для обработки выбран CSV-файл.")
    elif choice == '3':
        files = get_files_in_directory(data_directory, ['.xlsx'])
        if not files:
            print("Не найдено ни одного XLSX-файла в директории.")
            return
        print("Доступные XLSX-файлы:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        file_choice = int(input("Введите номер файла: ")) - 1
        if file_choice < 0 or file_choice >= len(files):
            print("Неверный выбор файла.")
            return
        file_path = os.path.join(data_directory, files[file_choice])
        transactions = load_transactions_from_xlsx(file_path)
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Пожалуйста, выберите правильный пункт меню.")
        return

    available_statuses = ["executed", "canceled", "pending"]
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы:")
    for i, status in enumerate(available_statuses, start=1):
        print(f"{i}. {status.upper()}")

    status_choice = int(input("Введите номер статуса: ")) - 1
    if status_choice < 0 or status_choice >= len(available_statuses):
        print("Неверный выбор статуса.")
        return

    status = available_statuses[status_choice]
    filtered_transactions = filter_transactions_by_status(transactions, status)
    print(f"Операции отфильтрованы по статусу \"{status.upper()}\"")

    sort_by_date = input("Отсортировать операции по дате? Да/Нет: ").lower()
    if sort_by_date == 'да':
        sort_order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        if sort_order == 'по возрастанию':
            filtered_transactions = sort_transactions_by_date(filtered_transactions, ascending=True)
        elif sort_order == 'по убыванию':
            filtered_transactions = sort_transactions_by_date(filtered_transactions, ascending=False)

    ruble_only = input("Выводить только рублевые транзакции? Да/Нет: ").lower()
    if ruble_only == 'да':
        filtered_transactions = filter_ruble_transactions(filtered_transactions)

    filter_by_description = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower()
    if filter_by_description == 'да':
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
