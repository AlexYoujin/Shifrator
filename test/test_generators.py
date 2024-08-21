import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 791923212,
            "state": "EXECUTED",
            "date": "2019-06-08T16:32:22.850589",
            "operationAmount": {
                "amount": "10451.88",
                "currency": {"name": "EUR", "code": "EUR"},
            },
            "description": "Перевод с карты на карту",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
    ]


def test_filter_by_currency(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)
    assert len(result) == 2
    for txn in result:
        assert txn["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_matching_currency(transactions):
    eur_transactions = filter_by_currency(transactions, "EUR")
    result = list(eur_transactions)
    assert len(result) == 1
    for txn in result:
        assert txn["operationAmount"]["currency"]["code"] == "EUR"


def test_filter_by_currency_empty_list():
    transactions = []
    usd_transactions = filter_by_currency(transactions, "USD")
    result = list(usd_transactions)
    assert len(result) == 0


def test_transaction_descriptions(transactions):
    descriptions = transaction_descriptions(transactions)
    result = list(descriptions)
    assert len(result) == 3
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]


def test_transaction_descriptions_empty_list():
    transactions = []
    descriptions = transaction_descriptions(transactions)
    result = list(descriptions)
    assert len(result) == 0


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999999999999995,
            9999999999999999,
            [
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ],
)
def test_card_number_generator(start, end, expected):
    generator = card_number_generator(start, end)
    result = list(generator)
    assert result == expected
